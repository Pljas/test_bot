#!/bin/bash
set -e

# Create and activate virtual environment
python -m venv /opt/venv
source /opt/venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the bot
exec python -u run.py