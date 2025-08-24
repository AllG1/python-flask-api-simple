# Get environment variables
source ./build/.env
# Clear current docker container & image
docker rm -f python-flask-api-mockup-container
docker rm -f python-flask-api-mockup-mysql
docker rmi python-flask-api-mockup-container-img:$VERSION
docker rmi python-flask-api-mockup-mysql-img:$VERSION
docker container prune --force --filter label=python-flask-api-mockup-container:$VERSION
docker container prune --force --filter label=python-flask-api-mockup-mysql:$VERSION
# Build new docker image
docker build -t python-flask-api-mockup-container-img:$VERSION -f ./build/app.dockerfile .
docker build -t python-flask-api-mockup-mysql-img:$VERSION -f ./build/mysql.dockerfile .
