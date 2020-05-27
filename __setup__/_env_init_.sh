#!/bin/bash

while getopts c:n:p: option; do
    case "${option}" in
        c) CREATE_ENV="${OPTARG}";;
        n) ENV_NAME="${OPTARG}";;
        p) ENV_PATH="${OPTARG}";;
    esac
done

if [ $CREATE_ENV -eq 1 ]; then 
    # Creating virtual environment
    echo "Creating virtual Environment..."
    python3 -m venv $ENV_NAME

    # Assigning env name to path
    ENV_PATH=$ENV_NAME
fi

# Activating virtual environment
echo "Activating Virtual Environment..."
source $ENV_PATH/bin/activate

# Installing dependencies in virtual environment
echo "Starting Installation for dependencies in $ENV_PATH"
pip3 install -r requirements.txt

# Deactivating virtual environment
echo "Deactivating virtual environment..."
deactivate

