#!/bin/bash

pip install -r requirements.txt
cd src
python main.py
cd -
echo "Project has been executed successfully!"