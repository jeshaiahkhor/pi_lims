#!/bin/bash
# Automated script to start the master venv, run the scanner, close the venv, and delete the oldest line (if over threshold)
file_name=scan_log.csv
threshold=2000

# If not already there, move to home directory
cd /home/pi

# Enable venv
. ./master_venv/bin/activate

# Run the script
python /home/pi/development/file_scan/modify_scan.py

# Deactivate the venv when done
deactivate

# Finding current number of lines - if past threshold, clear oldest line
current_lines=$(grep -c . $file_name)

if (($current_lines >= threshold)); then
	sed -i '2d' $file_name
fi
