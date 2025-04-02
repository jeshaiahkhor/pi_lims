# Importing modules
import os 
import glob

# Setting variables
directory_location = "/home/pi/data_files/*"

# Checking logfile for most recent update

# Printing file results from directory location
for file in glob.glob(directory_location):
    mod_time = os.path.getmtime(file)
    print(mod_time)

# Updating logfile with check details
