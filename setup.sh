#!/bin/bash

# For Ubuntu 16.04
sudo apt-get install mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8 virtualenv python3-pip

# For Ubuntu 14.04
#sudo apt-get install mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8 python-virtualenv python3-pip

virtualenv --python=$(which python3) .venv
. .venv/bin/activate
pip install wheezy.web gunicorn mecab-python3
