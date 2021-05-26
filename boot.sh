#!/bin/bash

python -m venv venv
venv/bin/pip install -q -r requirements.txt
source venv/bin/activate
cd app
flask run
