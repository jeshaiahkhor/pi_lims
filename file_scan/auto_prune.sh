#!/bin/bash
# Automatically runs CSV pruning script.

# Navigating to home directory
cd /home/pi/

# Activating virtual environment
. ./master_venv/bin/activate

# Running python script
python /home/pi/development/file_scan/log_prune.py

# Deactivating virtual environment
deactivate
