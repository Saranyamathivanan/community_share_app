# CommunityShare
A web application to collect and share geo tagged local knowledge

# Instructions to start the backend server

git clone https://github.com/AkhilM2020/community-share-app.git

cd community-share-app/backend/

sudo add-apt-repository universe

sudo apt install python3-pip -y

pip3 install -r requirements.txt --break-system-packages

sudo pip install awscli --break-system-packages

sudo apt install uvicorn

sudo apt install net-tools

 sudo pip install awscli --break-system-packagesgit
 
 cd community-share-app/backend/app
 
 cd uvicorn main:app --host 0.0.0.0 --port 8080
