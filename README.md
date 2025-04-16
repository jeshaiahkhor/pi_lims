# Pi-side software of LIMS

## Repository description 
Contains the files required for the Pi (or machine) side of the LIMS. 


## Functionality overview
This repo allows the Pi to scan files (dummy for now, but will be replaced with real data files) from a folder (right now the `/home/pi/data_files/` directory), detect when new files more recent than the last scan date logged (in the `scan_log.csv` file) have appeared in the folder,
and transfer new files to a central server (the mini PC in this case).

The repo repeatedly scans a folder for new files and sends detected files to the server, archiving the local copies. The local copies are kept for up to a week, after which they are cleared - every Monday at 12:00 am. 
The `scan_log.csv` file (ignored by Git for security) is kept to a maximum length of 2001 lines, pruned every 48 hours to keep only the most recent 2000 scan logs.


## File contents
The repo runs on 6 main files, detailed below.


### Bash scripts
📄 `archive_clear.sh` - File archiver; clears all files in the `/home/pi/data_files/archive/` directory when run.

📄 `auto_scan.sh` - File scanner & transferrer; activates the master `venv`, runs the `modify_scan.py` script, and deactivates the master `venv`.


### Python files
📄 `modify_scan.py` - Scans the `/home/pi/data_files/` directory for the last modified date of all files (excluding those in the `/archive/` directory). 
Files with last modified dates more recent than the time of the current run are sent via Fabric/Paramiko's SSH protocols to the `/home/nl_jesh/raw_data_central/` directory of the mini PC. 
The local file is then moved to the `/home/pi/data_files/archive/` directory. Also updates the log file `scan_log.csv` with details of the most recent run.


### Crontab file
📄 `crontab.bak` - Serves as an example `crontab` file to be copied - runs the file archiver script `archive_clear.sh` every week (on Monday), runs the CSV pruner script `auto_prune.sh` every 2 days, 
and runs the file scanning & transfer script `log_prune.py` every 5 minutes.

### Other files (not included in directory)
📄 `scan_log.csv` - A log of recent scans. Needs to be initialized with a header row, and a line of 0s as a starting point. 
