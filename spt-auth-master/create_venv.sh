#!/usr/bin/env bash

# creating virtual env
virtualenv venv

# going-in virtual env
source venv/bin/activate

# installing dependencies
pip install -r requirements.txt

# going-off virtual env
deactivate