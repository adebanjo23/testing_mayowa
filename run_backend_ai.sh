#!/bin/bash

# Define the repository and directory
REPO="git@github.com:Adamant-Code/cleona-backend-ai.git"
DIR="cleona-backend-ai" # Change this to your repository's directory name

# Setup SSH key
SSH_KEY_PATH="$(pwd)/.ssh/id_ed25519_three"
export GIT_SSH_COMMAND="ssh -i $SSH_KEY_PATH -o IdentitiesOnly=yes"

# Check if the repository directory exists
if [ ! -d "$DIR" ]; then
    echo "Repository directory does not exist. Cloning repository..."
    git clone $REPO $DIR
    cd $DIR
    # Checkout to the develop branch after cloning
    git checkout develop
else
    echo "Repository directory exists. Pulling latest changes..."
    cd $DIR
    git checkout develop
    git pull
fi

# Stop any running Docker Compose services
echo "Stopping any running Docker Compose services..."
docker-compose down

# Build and run services with Docker Compose
echo "Building and starting services with Docker Compose..."
docker-compose up --build -d

# Note: The '-d' flag in 'docker-compose up' runs the containers in the background
