# Importing modules
import os 
import csv
import glob
import time
from fabric import Connection

# Setting variables & creating objects
directory_location = "/home/pi/data_files/*.*"      # ensures only files, not directories, are scanned
server_location = "/home/nl_jesh/raw_data_central"
logfile = "/home/pi/development/file_scan/scan_log.csv"
archive_dir = "archive"
# Replace this with something more secure
remote = Connection(host="10.1.1.20", user="nl_jesh", port=14986, connect_kwargs={"key_filename": "/home/pi/.ssh/rpi01"})


# Function - cleans the \n off a line and splits it by ", " 
def clean_csv_line(str_input):
    return str_input.replace("\n", "").split(", ")

# Function - adds the archive directory to a filepath
def archive_location_update(filename, archive_dir):
    split_file = filename.split("/")
    update_list = split_file[:-1] + [archive_dir] + [split_file[-1]]
    return "/".join(update_list)


# Checking logfile for most recent update
with open(logfile, "r") as f:
    # Reading header line & identifying relevant columns for datetime and scan number.
    header = clean_csv_line(f.readline())
    
    datetime_idx = header.index("datetime")
    scan_num_idx = header.index("scan_number")
    
    # Retrieving last line (most recent scan) datetime details
    latest_scan_details = clean_csv_line(f.readlines()[-1])
    latest_scan_num = int(latest_scan_details[scan_num_idx])
    latest_scan_datetime = float(latest_scan_details[datetime_idx])

# Initializing parameters
success_status = 0
scan_time = time.time()
file_counter = 0                                    # Initializing
detection_list = []

# For each file found in the directory...
for file_name in glob.glob(directory_location):
    # Displaying current file being scanned
    print("Currently scanning: " + file_name)
    
    # Getting the modification time of all files
    mod_time = os.path.getmtime(file_name)

    # If the file mod time is more recent than the latest scan time...
    if mod_time > latest_scan_datetime:
        # Increment counter for new files detected
        file_counter += 1
        
        # Transfer file using Fabric SSH connection
        remote.put(file_name, server_location)
        
        # Log the transferred filename
        detection_list.append(file_name)
        
        # Print that the file has been sent
        print("Uploaded!")

        # Move the local copy of the file to the archive (os.replace for cross-platform)
        updated_archive_location = archive_location_update(file_name, archive_dir)
        os.replace(file_name, updated_archive_location)
        print("Archived!\n")
    else: 
        # Print that this file has been ignored
        print("Ignored - too ancient.\n")

# Setting success status to 1 if a non-zero quantity of files were copied.
if len(detection_list) > 0:
    success_status = 1

# Creating an update line for the scan log
update_line = [latest_scan_num + 1, scan_time, " | ".join(detection_list), success_status]

# Updating logfile with one new row of latest check details
with open(logfile, "a") as f:
    f.write(str(update_line).strip("[]"))
    f.write("\n")

# Close the SSH connection
remote.close()
