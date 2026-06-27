# CommunityShare

A cloud-based web application to collect, preserve, and share geo-tagged indigenous and local community knowledge.

## Overview

Around the world, indigenous and local communities hold traditional knowledge passed down through generations — from native plants and animals to cultural landmarks, folklore, and historical stories. CommunityShare is a scalable, secure AWS-based platform that helps communities worldwide document and preserve this knowledge before it is lost.

Users can capture photos and stories tied to specific locations, all geo-tagged and visualized on an interactive map — similar to how Airbnb shows property listings.

## Features

- Geo-tagged knowledge entries with interactive map view
- Upload photos, audio, and video linked to locations
- User authentication and access control
- Search and filter community knowledge
- Secure cloud storage for all media and metadata
- CI/CD pipeline for automated deployments

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI, Uvicorn |
| Database | Amazon DynamoDB |
| Storage | Amazon S3, CloudFront |
| Auth | Amazon Cognito |
| Maps | Amazon Location Service, MapLibre GL |
| Search | Elasticsearch Service |
| Notifications | Amazon SNS |
| Monitoring | Amazon CloudWatch |
| CI/CD | AWS CodePipeline, CodeBuild |
| Security | AWS IAM, Secrets Manager |


## Getting Started

### Prerequisites

- Python 3.x
- pip
- AWS CLI configured
- uvicorn

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/AkhilM2020/community-share-app.git
cd community-share-app/backend/

# Install Python and pip
sudo add-apt-repository universe
sudo apt install python3-pip -y

# Install dependencies
pip3 install -r requirements.txt --break-system-packages

# Install AWS CLI
sudo pip install awscli --break-system-packages

# Install uvicorn
sudo apt install uvicorn

# Start the backend server
cd app
uvicorn main:app --host 0.0.0.0 --port 8080
```

### Access the App

Once running, open your browser and go to:
```
http://localhost:8080
```




