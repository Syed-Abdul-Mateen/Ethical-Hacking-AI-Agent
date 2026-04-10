#!/bin/bash
# Install OS dependencies for development

# Update package list
sudo apt update

# Install essential tools
sudo apt install -y git curl wget python3 python3-pip python3-venv php-cli nodejs npm

# Install Python dependencies
pip3 install -r requirements.txt

echo "Environment setup complete."