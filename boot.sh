#!/bin/bash

python -m venv venv
venv/bin/pip install -q -r requirements.txt
source venv/bin/activate
if ! [[ -d migrations ]]
then
  flask db init > /dev/null 2>&1
  flask db migrate > /dev/null 2>&1
  flask db upgrade > /dev/null 2>&1
fi
cd app
flask run
