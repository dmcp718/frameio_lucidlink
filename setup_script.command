#!/bin/zsh

# Check if Homebrew is installed
if ! command -v brew &> /dev/null
then
    echo "Homebrew is not installed. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install Python 3.10.13
brew install python@3.10

# Create a virtual environment
/usr/local/opt/python@3.10/bin/python3.10 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the modules from requirements.txt
pip install -r requirements.txt