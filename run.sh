#!/bin/bash

sudo .venv/bin/gunicorn -b0.0.0.0:80 \
  --pid gunicorn.pid \
  --daemon \
  --threads 30 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  web:main
