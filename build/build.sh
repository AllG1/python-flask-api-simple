# Get environment variables
source ./build/.env
# Clear current docker container & image
docker rm -f python-flask-api-mockup-container
docker rmi python-flask-api-mockup-container-img:$VERSION
docker container prune --force --filter label=python-flask-api-mockup-container:$VERSION
# Build new docker image
docker build -t python-flask-api-mockup-container-img:$VERSION -f ./build/Dockerfile .