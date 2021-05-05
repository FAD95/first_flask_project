#!/bin/bash

#pip install -r requierements.txt
#source venv/bin/activate

export FLASK_APP=main.py
export FLASK_DEBUG=0
export FLASK_ENV=production

flask run