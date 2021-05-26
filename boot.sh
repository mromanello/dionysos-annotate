#!/bin/bash

python -m venv venv
venv/bin/pip install -r requirements.txt
source venv/bin/activate
if ! [[ -d migrations ]]
then
  flask db init
  flask db migrate
  flask db upgrade
fi
cd app
flask run
