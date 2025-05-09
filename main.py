"""
    Ideas:
    determine if time zone uses daylight savings and adjust from that point
    slider y/n for if you want to adjust for daylight savings

    steps:
    understand logic of user choosing a timezone and it changes the time that gets displayed
    design interface so that timezone gets changed by clicking rectangles
    design clock pattern so that it updates live and looks like a clock (while(True))?
    publish as website?
"""

import time
from datetime import datetime, tzinfo, timedelta
from pathlib import Path
import json
from tkinter import *
from tkinter import ttk
import tkinter as tk

#list of accepted timezones and how they relate to the UTC (coordinated universal time)
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

#converts timezones to a json
path = Path("timezone_offsets.json")
contents = json.dumps(timezone_offsets)
path.write_text(contents)

class Clock():
    def __init__(self, tz = "UTC"):
        self.tz = tz.upper()
        self.y = 5  # y-pos
        self.c = 5  # counter
        #creating gui
        self.root = Tk()
        self.frm = ttk.Frame(self.root, padding=20)
        self.frm.grid()
        ttk.Button(self.frm, text="Quit", command=self.root.destroy).grid(column=2, row=0)
        ttk.Button(self.frm, text="Start Clock", command=self.write).grid(column=1, row=0)
        # canvas
        self.canvas = tk.Canvas(self.frm, height=800, width=800)
        #not sure what this line does
        self.canvas.bind("<Configure>", lambda e:self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        #keeps code responsive
        self.root.mainloop()

    def write(self):
        if self.c > 0:
            for i in range (10):
                ttk.Label(self.frm, text = "0").grid(column = 10, row = i)
            for i in range (7):
                ttk.Label(self.frm, text = "3").grid(column = 10 + i, row = 10)
            self.c -= 1  # reduce counter
            self.after(1000, self.write)  # call again in 1 second
        else:
            self.c = 5   # when counter is 0 reset counter which allows to run infinitely without crashing (while true didn't work)
            self.write()




    #updates current_UTC to whatever the system time is
    def update_time(self):
        offset = timezone_offsets[self.tz]
        # Get current UTC time in seconds since epoch
        utc_seconds_since_epoch = time.time()
        print(f"Seconds since epoch: {utc_seconds_since_epoch}")

        # Convert time to UTC time string
        UTC_time_string = time.asctime(time.gmtime(utc_seconds_since_epoch))
        print(f"UTC time: {UTC_time_string}")

        # prints string of local time
        current_time = datetime.now()
        print(f"local time: {datetime.ctime(current_time)}")

        #print inputted timezone time (times 3600 to convert hours into seconds)
        tz_seconds_since_epoch = time.time() + (offset * 3600)
        print(f"timezone seconds since epoch: {tz_seconds_since_epoch}")
        tz_time_string = time.asctime(time.gmtime(tz_seconds_since_epoch))
        print(f"Timezone time: {tz_time_string}")

    def print_timezone_options():
        for key, value in timezone_offsets.items():
            print(f"{key}: {value} hours away from UTC")

def main():
    UTC_clock = Clock()


"""
    #default prints seconds since epoch, local time, and utc time
    update_time()
    #get user's preferred timezone
    print_timezone_options()
    tz_acronyms = timezone_offsets.keys()
    current_timezone = input("Which of these timezones do you want to display? (write acronym) ")
    while(current_timezone.upper() not in tz_acronyms):
        print("Not a valid acronym! Try again... ")
        current_timezone = input("Which of these timezones do you want to display? (write acronym) ")
    #prints seconds since epoch, local time, utc time, and selected timezone time
    update_time(timezone_offsets[current_timezone.upper()])
"""

if __name__ == "__main__":
    main()