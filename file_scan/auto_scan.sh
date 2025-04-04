#!/bin/bash
# Automated script to start the master venv, run the scanner, and close the venv

# If not already there, move to home directory
cd /home/pi

# Enable venv
. ./master_venv/bin/activate

# Run the script
python /home/pi/development/file_scan/modify_scan.py

# Deactivate the venv when done
deactivate
