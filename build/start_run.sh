# Get environment variables
source ./build/.env

# Run container with docker-compose.yml
docker-compose -f ./build/docker-compose.yml up -d

# Check loaded containers
sleep 1
docker ps -a

# show ending message
echo "All containers are up and running."