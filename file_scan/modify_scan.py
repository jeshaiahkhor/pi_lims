# Importing modules
import os 
import csv
import glob
#from fabric import Connection

# Setting variables & creating objects
directory_location = "/home/pi/data_files/*.*"      # ensures only files, not directories, are scanned
logfile = "scan_log.csv"
#remote = Connection()

# Function - cleans the \n off a line and splits it by ", " 
def clean_csv_line(str_input):
    return str_input.replace("\n", "").split(", ")


# Checking logfile for most recent update
with open(logfile, "r") as f:
    # Reading header line & identifying relevant column for datetime
    header = clean_csv_line(f.readline())
    datetime_idx = header.index("Datetime")
    
    # Retrieving last line (most recent scan) datetime details
    latest_scan = clean_csv_line(f.readlines()[-1])
    print(latest_scan)
    latest_scan_datetime = float(latest_scan[datetime_idx])
    print(latest_scan_datetime)

# Printing file results from directory location
file_counter = 0                                    # Initializing
detection_list = []
for file_name in glob.glob(directory_location):
    print(file_name)
    mod_time = os.path.getmtime(file_name)
    print(mod_time)
    if mod_time > latest_scan_datetime:
        # Increment counter for new files detected
        file_counter += 1
        
        # Transfer file
        
        # Log the transferred filename
        detection_list.append(file_name)
        
print(file_counter, detection_list)
# Updating logfile with one new row of latest check details


# Printing section to verify
