"""
    Ideas:
    go off of UTC
    add hours depending on time zone chosen
    determine if time zone uses daylight savings and adjust from that point
    slider y/n for if you want to adjust for daylight savings

    steps:
    understand logic of user choosing a timezone and it changes the time that gets displayed
    design interface so that timezone gets changed by clicking rectangles
    design clock pattern so that it updates live and looks like a clock
    publish as website?
"""

import tkinter as tk
import time
from datetime import datetime
from pathlib import Path
import json

timezone_offsets = {
    "UTC": 0,        # Coordinated Universal Time
    "CET": 1,        # Central European Time
    "EET": 2,        # Eastern European Time
    "MSK": 3,        # Moscow Standard Time
    "GST": 4,        # Gulf Standard Time
    "IST": 5.5,      # India Standard Time
    "BST (BD)": 6,   # Bangladesh Standard Time
    "ICT": 7,        # Indochina Time
    "CST (China)": 8,# China Standard Time
    "JST": 9,        # Japan Standard Time
    "AEST": 10,      # Australian Eastern Standard Time
    "NZST": 12,      # New Zealand Standard Time
    "NST": -3.5,     # Newfoundland Standard Time
    "ART": -3,       # Argentina Time
    "AST": -4,       # Atlantic Standard Time
    "EST": -5,       # Eastern Standard Time
    "CST": -6,       # Central Standard Time
    "MST": -7,       # Mountain Standard Time
    "PST": -8,       # Pacific Standard Time
    "AKST": -9,      # Alaska Standard Time
    "HST": -10       # Hawaii Standard Time
}

path = Path("timezone_offsets.json")
contents = json.dumps(timezone_offsets)
path.write_text(contents)

print(contents)

def update_time(timezone = 0):
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
