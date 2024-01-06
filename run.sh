#!/bin/bash
nohup redis-server &
celery -A app worker --loglevel DEBUG &
flask run --reload
