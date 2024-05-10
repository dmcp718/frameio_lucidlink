#!/bin/zsh

# Check if Homebrew is installed
if ! command -v brew &> /dev/null
then
    echo "Homebrew is not installed. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Check if Python 3.10 is installed
if ! brew list python@3.10 &> /dev/null
then
    echo "Python 3.10 is not installed. Installing Python 3.10..."
    brew install python@3.10
fi

# Check if the virtual environment exists
if [ ! -d "venv" ]
then
    echo "Virtual environment does not exist. Creating a new virtual environment..."
    /usr/local/opt/python@3.10/bin/python3.10 -m venv venv
fi

# Check if the requirements.txt file exists
if [ -f "requirements.txt" ]
then
    echo "Installing modules from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping module installation."
fi