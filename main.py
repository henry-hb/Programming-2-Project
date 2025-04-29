"""
    Ideas:
    go off of UTC
    add hours depending on time zone chosen
    determine if time zone uses daylight savings and adjust from that point

"""

import tkinter as tk
import time
from datetime import datetime

def update_time():
    current_UTC = datetime.now()
    print(f"local time: {datetime.ctime(current_UTC)}")

def main():
    
    # Get current time in seconds since epoch
    seconds_since_epoch = time.time()
    print(f"Seconds since epoch: {seconds_since_epoch}")

    # Convert time to local time string
    local_time_string = time.ctime(seconds_since_epoch)
    print(f"Local time: {local_time_string}")

    update_time()

if __name__ == "__main__":
    main()