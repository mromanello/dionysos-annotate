#!/bin/bash

python -m venv venv
venv/bin/pip install -q -r requirements.txt
source venv/bin/activate
cd app
# uncomment line below to switch to dev behaviour
#export FLASK_ENV=development
flask run
