#!/bin/sh

source venv/bin/activate
celery -A cectf_proxy worker --loglevel=info
