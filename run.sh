#!/bin/sh

source venv/bin/activate
export FLASK_APP=cectf_proxy
export FLASK_ENV=development
export FLASK_RUN_PORT=80
flask run
