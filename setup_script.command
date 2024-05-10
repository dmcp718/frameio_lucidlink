#!/bin/zsh

# Check if Homebrew is installed
if ! command -v brew &> /dev/null
then
    echo "Homebrew is not installed. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" && \
    echo "Homebrew installed successfully." || \
    { echo "Failed to install Homebrew. Exiting."; exit 1; }
fi

# Check if Python 3.10 is installed
if ! brew list python@3.10 &> /dev/null
then
    echo "Python 3.10 is not installed. Installing Python 3.10..."
    brew install python@3.10 && \
    echo "Python 3.10 installed successfully." || \
    { echo "Failed to install Python 3.10. Exiting."; exit 1; }
fi

# Check if the virtual environment exists
if [ ! -d "venv" ]
then
    echo "Virtual environment does not exist. Creating a new virtual environment..."
    python3.10 -m venv venv && \
    echo "Virtual environment created successfully." || \
    { echo "Failed to create virtual environment. Exiting."; exit 1; }
fi

# Check if the requirements.txt file exists
if [ -f "requirements.txt" ]
then
    echo "Installing modules from requirements.txt..."
    source venv/bin/activate && \
    pip install -r requirements.txt && \
    echo "Modules installed successfully." || \
    { echo "Failed to install modules from requirements.txt. Exiting."; exit 1; }
else
    echo "requirements.txt not found. Skipping module installation."
fi