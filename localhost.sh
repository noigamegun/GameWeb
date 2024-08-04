#!/bin/bash

# Check if python3 is installed
if ! command -v python3 --version > /dev/null; then
    echo "Python3 is not installed. Exiting..."
    exit 1
fi

python3 -m http.server $PORT
