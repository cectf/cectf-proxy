#!/bin/sh

python3 -m venv venv
source venv/bin/activate

pip install -e .

mkdir instance
echo "CECTF_FRONTEND_URL = 'http://127.0.0.1:5000'" >> instance/config.py
echo "CECTF_SERVER_URL = 'http://127.0.0.1:5001'" >> instance/config.py
