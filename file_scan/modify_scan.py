# Importing modules
import os 
import csv
import glob

# Setting variables
directory_location = "/home/pi/data_files/*"
logfile = "scan_log.csv"

# Checking logfile for most recent update
with open(logfile, "r") as f:
    last_line = f.readlines()[-1]
    print(last_line)

# Printing file results from directory location
for file in glob.glob(directory_location):
    mod_time = os.path.getmtime(file)
    print(mod_time)

# Updating logfile with one new row of latest check details
