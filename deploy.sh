#!/bin/bash

# Variables
REMOTE_HOST=""
REMOTE_DIR=""
GIT_BRANCH="master"

# SSH and run commands on remote host
ssh $REMOTE_HOST << EOF
  # Navigate to project directory
  cd $REMOTE_DIR
  
  sudo su
  
  # Fetch and pull changes from GitHub while preserving local changes
  git fetch origin $GIT_BRANCH
  git stash  # Stash any local changes
  git pull origin $GIT_BRANCH
  git stash pop  # Re-apply stashed changes (merge conflicts handled interactively)

  # Stop, rebuild, and restart Docker containers
  docker-compose down
  docker-compose up --build -d
EOF

echo "Deployment complete."