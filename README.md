# MachineLeaningProject
#This is First Machine Learning Project
Creating Conda environment
```
conda create -p env python==3.7 -y

conda activate env/
```

1. HEROKU_EMAIL = sameepkumarpanigrahi@gmal.com
2. HEROKU_APP_KEY = bbf6dacb-5270-49f7-9f46-4dc0001a3df8
3. HEROKU_APP_NAME = ml-regression-app

BUILD DOCKER IMAGE 
```
docker build -t <image_name>:<tagname> .
```
To List Docker Image
```
docker images
```
Run docker image
```
docker run -p 5000:5000 -e PORT=5000 f8c749e73678
```
To check running container in docker
```
docker ps
```
To stop docker conatiner
```
docker stop <container_id>
```