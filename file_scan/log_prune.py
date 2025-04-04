# Importing libraries
import pandas as pd
import numpy as np

# Defining constants
scanlog_path = "/home/pi/development/file_scan/scan_log.csv"
# test_path = "/home/pi/development/file_scan/scan_log_test.csv"
threshold = 600         # At a scanning rate of 1 scan/5 mins, this corresponds to 50 hrs

# Importing raw file (using pandas)
df = pd.read_csv(scanlog_path, sep=", ", engine="python")

# Finding most recent scan number
header_text = str(df.columns.values).strip("[]").replace("'", "").replace(" ", ", ")
latest_scan = df.scan_number.iloc[-1]
print("Latest Scan Number: ", latest_scan)

# If the scan number is bigger than the threshold...
if latest_scan > threshold:
    print("Threshold exceeded - pruning file.")
    trimmed_df = df[df.scan_number >= (latest_scan - threshold)]
    np.savetxt(scanlog_path, trimmed_df, fmt="%s", delimiter=", ", header=header_text, comments="")
else: 
    print("Under threshold - file maintained.")
    
