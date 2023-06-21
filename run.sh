#!/bin/sh
export FLASK_SECRET_KEY=1a2d5a33a7f02c888ff796a9f5f422bf96f4eb1c6
export PYTHONUNBUFFERED=1
export RCHILLI_API_KEY=00SLQQL6
git pull origin master
pip install -r requirements.txt
python3 -O flask_application/main.py