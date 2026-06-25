import os
import uuid
from fastapi import FastAPI, Query, Body,UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import boto3
from boto3.dynamodb.conditions import Key, Attr
from dotenv import load_dotenv
from botocore.exceptions import ClientError
from fastapi import Depends, HTTPException, Header
from jose import jwk, jwt
from jose.utils import base64url_decode
import json, urllib.request
from fastapi.responses import JSONResponse
load_dotenv()

# --- Config ---

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
TABLE_NAME = os.getenv("DYNAMODB_TABLE", "CommunityKnowledge")

# S3 settings
BUCKET_NAME = os.getenv("S3_BUCKET", "community-share-uploads")
BUCKET_CLOUD_FRONT_URL = os.getenv("CLOUDFRONT_URL", "d2ln0jlxttrevg.cloudfront.net")
#incognito settings
COGNITO_REGION = os.getenv("AWS_REGION", "us-east-1")
USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID","us-east-1_7qBM2q4n1")
APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID","4eum96s6s4qrehet5lcu1f2tjh")
ISSUER = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}"
JWKS_URL = f"{ISSUER}/.well-known/jwks.json"
_jwks = json.loads(urllib.request.urlopen(JWKS_URL).read().decode("utf-8"))

async def verify_jwt(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    token = authorization.split(" ", 1)[1]

    headers = jwt.get_unverified_header(token)
    kid = headers.get('kid')
    key = next((k for k in _jwks['keys'] if k['kid'] == kid), None)
    if not key:
        raise HTTPException(status_code=401, detail="Invalid token key")

    try:
        claims = jwt.decode(
            token,
            key,
            algorithms=['RS256'],
            audience=APP_CLIENT_ID,
            issuer=ISSUER
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {e}")
    return claims


# dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
# dynamodb = boto3.resource('dynamodb',
#                          endpoint_url='http://localhost:8000',
#                          region_name='us-east-1',
#                          aws_access_key_id='dummy',
#                          aws_secret_access_key='dummy')
# s3 = boto3.client("s3", region_name=AWS_REGION)



# --- Credential Handling ---
session_kwargs = {"region_name": AWS_REGION}

if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    # Use credentials from .env
    session_kwargs.update({
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY
    })
    print("🔑 Using credentials from .env file")
else:
    # Fallback to default AWS credential chain (~/.aws/credentials, env, IAM role)
    print("📂 Using AWS default credential chain (~/.aws/credentials, env, or IAM role)")

# Initialize session
session = boto3.Session(**session_kwargs)
dynamodb = session.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

s3 = session.client("s3")
s3_client = boto3.client("s3", region_name=AWS_REGION)

app = FastAPI(title="Community Share Backend")

# Allow frontend in S3/CloudFront to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure table exists
def create_table_if_not_exists():
    try:
        table = dynamodb.Table(TABLE_NAME)
        table.load()  # try to load metadata
        print(f"✅ Table {TABLE_NAME} already exists")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            print(f"⚠️ Table {TABLE_NAME} not found. Creating...")
            table = dynamodb.create_table(
                TableName=TABLE_NAME,
                KeySchema=[
                    {"AttributeName": "UserID", "KeyType": "HASH"},  # partition key
                    {"AttributeName": "RecordID", "KeyType": "RANGE"},  # sort key
                ],
                AttributeDefinitions=[
                    {"AttributeName": "UserID", "AttributeType": "S"},
                    {"AttributeName": "RecordID", "AttributeType": "S"},
                    {"AttributeName": "Country", "AttributeType": "S"},
                    {"AttributeName": "City", "AttributeType": "S"},                   
                ],
                ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
                GlobalSecondaryIndexes=[
                    {
                        "IndexName": "CountryIndex",
                        "KeySchema": [{"AttributeName": "Country", "KeyType": "HASH"}],
                        "Projection": {"ProjectionType": "ALL"},
                        "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
                    },
                    {
                        "IndexName": "CountryCityIndex",
                        "KeySchema": [
                            {"AttributeName": "Country", "KeyType": "HASH"},
                            {"AttributeName": "City", "KeyType": "RANGE"},
                        ],
                        "Projection": {"ProjectionType": "ALL"},
                        "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
                    },
                ],
            )
            table.wait_until_exists()
            print(f"✅ Created table {TABLE_NAME}")
        else:
            raise

# Run table check at startup
@app.on_event("startup")
def startup_event():
    create_table_if_not_exists()



# ----- Models -----
class KnowledgeItem(BaseModel):
    UserID: str
    Country: str
    City: str
    GeoLocation: str   # "lat,lon"
    S3ImageURL: str
    Description: str
    DetailedDescription: str
    Category: str
    KnowledgeType: str


# ----- Routes -----
@app.get("/search")
def search_items(
    country: Optional[str] = None,
    city: Optional[str] = None,
    category: Optional[str] = None,
    type: Optional[str] = Query(None, alias="knowledgeType"),
):
    print(f"Search params: country={country}, city={city}, category={category}, type={type}")
    """Search by filters (simple scan + filter)."""
    filter_expr = None
    if country:
        filter_expr = Attr("Country").eq(country)
    if city:
        expr = Attr("City").eq(city)
        filter_expr = expr if filter_expr is None else filter_expr & expr
    if category:
        expr = Attr("Category").eq(category)
        filter_expr = expr if filter_expr is None else filter_expr & expr
    if type:
        expr = Attr("KnowledgeType").eq(type)
        filter_expr = expr if filter_expr is None else filter_expr & expr

    if filter_expr:
        resp = table.scan(FilterExpression=filter_expr)
    else:
        resp = table.scan()
    print(f"Found {resp} items")
    return resp.get("Items", [])


@app.get("/bbox")
def bbox_query(
    minLng: float, minLat: float, maxLng: float, maxLat: float,
    user: Optional[str] = None,
    country: Optional[str] = None,
    city: Optional[str] = None,
    category: Optional[str] = None,
    type: Optional[str] = Query(None, alias="knowledgeType"),
):
    """Scan and return items within bounding box."""
    resp = table.scan()
    items = resp.get("Items", [])

    results = []
    for item in items:
        try:
            lat, lng = map(float, item["GeoLocation"].split(","))
            if minLat <= lat <= maxLat and minLng <= lng <= maxLng:
                results.append(item)
        except Exception:
            continue

    # optional filtering
    if user:
        results = [i for i in results if i["UserID"] == user]
    if country:
        results = [i for i in results if i["Country"] == country]
    if city:
        results = [i for i in results if i["City"] == city]
    if category:
        results = [i for i in results if i["Category"] == category]
    if type:
        results = [i for i in results if i["KnowledgeType"] == type]

    return results


@app.post("/upload/")
async def upload_file(
    image: UploadFile = File(...),
    UserID: str = Form(...),
    Country: str = Form(...),
    City: str = Form(...),
    GeoLocation: str = Form(...),
    Description: str = Form(...),
    DetailedDescription: str = Form(...),
    Category: str = Form(...),
    KnowledgeType: str = Form(...),
    claims: dict = Depends(verify_jwt)  # <- require valid JWT
):
    try:
        # Generate a unique filename
        file_extension = image.filename.split(".")[-1]
        file_key = f"uploads/{uuid.uuid4()}.{file_extension}"

        # Upload to S3
        s3_client.upload_fileobj(
            image.file,
            BUCKET_NAME,
            file_key,
            ExtraArgs={"ContentType": image.content_type}
        )

        # Generate S3 URL
        s3_url = f"https://{BUCKET_CLOUD_FRONT_URL}/{file_key}"
        print(f"Uploaded file to {s3_url}")
        # Save metadata to DynamoDB
        item = {
            "RecordID": str(uuid.uuid4()),
            "UserID": UserID,
            "Country": Country,
            "City": City,
            "GeoLocation": GeoLocation,
            "S3ImageURL": s3_url,
            "Description": Description,
            "DetailedDescription": DetailedDescription,
            "Category": Category,
            "KnowledgeType": KnowledgeType
        }
        table.put_item(Item=item)
        return {"status": "success", "item": item}
        # return JSONResponse(content={"message": "Upload successful", "data": item}, status_code=201)

    except Exception as e:
        return {"error": str(e), "status_code": 500}
        # return JSONResponse(content={"error": str(e)}, status_code=500)


@app.options("/upload/")
async def options_upload():
    # return JSONResponse(status_code=200)
    return JSONResponse(status_code=200)


@app.get("/health-check")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}
