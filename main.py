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
import math

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
    def __init__(self, tz = "UTC", daylight_savings = False):
        self.tz = tz.upper()
        self.daylight_savings = daylight_savings
        self.y = 5  # y-pos
        self.c = 5  # counter
        #creating gui
        self.root = Tk()
        self.root.geometry("800x800")
        self.root.title("World Clock")


        self.frm = ttk.Frame(self.root, padding=20)
        self.frm.place(x=0, y=0)
        quit = ttk.Button(self.frm, text="Quit", command=self.root.destroy)
        quit.place(x=20, y=20)
        start = ttk.Button(self.frm, text="Start Clock", command=self.write)
        start.place(x=100, y=20)
        # canvas
        self.canvas = tk.Canvas(self.frm, height=700, width=700)
        self.canvas.place(x=50, y=80)
        #resizes screen
        self.canvas.bind("<Configure>", lambda e:self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        #selects daylight savings
        ds_button = ttk.Button(self.frm, text="Toggle Daylight Savings", command=self.change_ds)
        ds_button.place(x=220, y=20)
        ds_label = ttk.Label(self.frm, text = f"Daylight Savings: {self.daylight_savings}")
        ds_label.place(x=400, y=20)

        #keeps code responsive
        self.root.mainloop()

    def write(self):
        self.canvas.delete("all")
        if self.c > 0:
            

            #times 6 because 60 seconds, but 360 degrees. plus 90 because sin/cos start on right but clock starts on top
            second_angle = math.radians(self.update_time()["Second"] * 6 + 90)
            minute_angle = math.radians(self.update_time()["Minute"] * 6 + 90)
            hour_angle = math.radians(self.update_time()["Hour"] * 30 + 90)
            if(self.update_time()["Second"] == 0):
                minute_angle += math.radians(6)
            if(self.update_time()["Minute"] == 0):
                hour_angle += math.radians(12)

            second_x = math.cos(second_angle) * 200 + 250
            second_y = math.sin(second_angle) * 200 + 250
            #self.canvas.coords(second_hand, second_x, second_y)

            minute_x  = math.cos(minute_angle) * 200 + 250
            minute_y = math.sin(minute_angle) * 200 + 250
            #self.canvas.coords(minute_hand, minute_x, minute_y)

            hour_x = math.cos(hour_angle) * 200 + 250
            hour_y = math.sin(hour_angle) * 200 + 250
            #self.canvas.coords(hour_hand, hour_x, hour_y)

            for i in range (10):
                hour_hand = ttk.Label(self.frm, text = self.update_time()["Hour"])
                hour_hand.place(x=hour_x,y=hour_y)
            for i in range (7):
                minute_hand = ttk.Label(self.frm, text = self.update_time()["Minute"])
                minute_hand.place(x=minute_x,y=minute_y)
            for i in range (5):
                second_hand = ttk.Label(self.frm, text = self.update_time()["Second"])
                second_hand.place(x=second_x,y=second_y)
            

            self.c -= 1  # reduce counter
            self.root.after(1000, self.write)  # call again in 1 second


        else:
            self.c = 5   # when counter is 0 reset counter which allows to run infinitely without crashing (while true didn't work)
            self.write()

    def change_ds(self):
        if self.daylight_savings:
            self.daylight_savings = False
        else:
            self.daylight_savings = True
    
        ds_label = ttk.Label(self.frm, text = f"Daylight Savings: {self.daylight_savings}").grid(column = 4, row = 0)


    def update_position(self, second_angle):
        #times 6 because 60 seconds, but 360 degrees. plus 90 because sin/cos start on right but clock starts on top
        second_angle = self.update_time()["Second"] * 6 + 90
        minute_angle = self.update_time()["Minute"] * 6 + 90
        hour_angle = self.update_time()["Hour"] * 30 + 90
        if(self.update_time()["Second"] == 0):
            minute_angle += 6
        if(self.update_time()["Minute"] == 0):
            hour_angle += 12

        second_x = math.cos(second_angle) * 200 + 250
        second_y = math.sin(second_angle) * 200 + 250
        self.canvas.coords(self.second_hand, second_x, second_y)

        minute_x  = math.cos(minute_angle) * 200 + 250
        minute_y = math.sin(minute_angle) * 200 + 250
        self.canvas.coords(self.minute_hand, minute_x, minute_y)

        hour_x = math.cos(hour_x) * 200 + 250
        hour_y = math.sin(hour_y) * 200 + 250
        self.canvas.coords(self.hour_hand, hour_x, hour_y)

        self.canvas.after(1000, self.update_position)


    #updates current_UTC to whatever the system time is
    def update_time(self):
        offset = timezone_offsets[self.tz]
        # Get current UTC time in seconds since epoch
        utc_seconds_since_epoch = time.time()

        #print inputted timezone time (times 3600 to convert hours into seconds)
        tz_seconds_since_epoch = time.time() + (offset * 3600)
        tz_time_string = time.asctime(time.gmtime(tz_seconds_since_epoch))

        #return dictionary of current hour, minute, seconds
        if self.daylight_savings:
            time_dict = {"Hour":(math.floor((tz_seconds_since_epoch / 3600) % 24) + 1),
                        "Minute":(math.floor((tz_seconds_since_epoch / 60) % 60)),
                        "Second":(math.floor(tz_seconds_since_epoch % 60))}
            return time_dict
        else:
            time_dict = {"Hour":(math.floor((tz_seconds_since_epoch / 3600) % 24)),
                        "Minute":(math.floor((tz_seconds_since_epoch / 60) % 60)),
                        "Second":(math.floor(tz_seconds_since_epoch % 60))}
            return time_dict

    #just for testing
    def print_timezone_options():
        for key, value in timezone_offsets.items():
            print(f"{key}: {value} hours away from UTC")

def main():
    UTC_clock = Clock("PST", True)

if __name__ == "__main__":
    main()