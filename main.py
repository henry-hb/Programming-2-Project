"""
    Ideas:
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
import streamlit as st

#creating website layout
st.header("World Clock!", divider="rainbow")
st.subheader("Made by Henry Hall-Brown")

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
    def __init__(self, tz="UTC", daylight_savings=False):
        self.tz = tz.upper()
        self.daylight_savings = daylight_savings
        self.y = 5
        self.c = 5

        # Create root window
        self.root = tk.Tk()
        self.root.geometry("800x800")
        self.root.title("World Clock")

        # Create frame and place it
        self.frm = ttk.Frame(self.root)
        self.frm.place(x=0, y=0, width=800, height=800)

        # Quit Button
        quit_btn = ttk.Button(self.frm, text="Quit", command=self.root.destroy)
        quit_btn.place(x=20, y=20)

        # Start Clock Button
        start_btn = ttk.Button(self.frm, text="Start Clock", command=self.write)
        start_btn.place(x=100, y=20)

        # Toggle Daylight Savings Button
        ds_button = ttk.Button(self.frm, text=f"Toggle Daylight Savings (Current: {self.daylight_savings})", command=self.change_ds)
        ds_button.place(x=180, y=20)

        # Canvas for drawing the clock
        self.canvas = tk.Canvas(self.frm, width=700, height=700, bg="white")
        self.canvas.place(x=50, y=70)

        #dropdown menu for timezones
        timezones = timezone_offsets.keys() 
        self.opt = tk.StringVar(value=self.tz)
        dropdown = OptionMenu(self.root, self.opt, *timezones)
        dropdown.place(x=400,y=20)
        self.tz = self.opt.get()

        self.root.mainloop()

    #updates current daylight savings
    def change_ds(self):
        self.daylight_savings = not self.daylight_savings
        ds_button = ttk.Button(self.frm, text=f"Toggle Daylight Savings (Current: {self.daylight_savings})", command=self.change_ds)
        ds_button.place(x=180, y=20)

    def write(self):
        self.tz = self.opt.get()
        #creates circle outline of clock
        circle_id = self.canvas.create_oval(150, 35, 550, 435, fill="white", outline="black")
        #removes everything from canvas so no labels repeat
        for widget in self.frm.winfo_children():
            # Check if the widget is a Label (ttk.Label or tk.Label)
            if isinstance(widget, (ttk.Label, tk.Label)):
                widget.destroy()  # removes the label from the GUI
        #c is a counter so this code can run forever but not glitch out with a while(True) or something like that
        if self.c > 0:
            #times 6 because 60 seconds, but 360 degrees. plus 90 because sin/cos start on right but clock starts on top
            second_angle = math.radians(self.update_time()["Second"] * 6 - 90)
            minute_angle = math.radians(self.update_time()["Minute"] * 6 - 90)
            hour_angle = math.radians(self.update_time()["Hour"] * 30 - 90)
            if(self.update_time()["Second"] == 0):
                minute_angle += math.radians(6)
            if(self.update_time()["Minute"] == 0):
                hour_angle += math.radians(12)
            
            #creates all clock hands
            for i in range (1,6):
                #multiplied by i * 20 so that they are all in a line
                hour_x = math.cos(hour_angle) * (i*20) + 400
                hour_y = math.sin(hour_angle) * (i*20) + 300
                hour_hand = ttk.Label(self.frm, text = self.update_time()["Hour"])
                hour_hand.place(x=hour_x,y=hour_y)
            for i in range (1,8):
                minute_x  = math.cos(minute_angle) * (i*20) + 400
                minute_y = math.sin(minute_angle) * (i*20) + 300
                minute_hand = ttk.Label(self.frm, text = self.update_time()["Minute"])
                minute_hand.place(x=minute_x,y=minute_y)
            for i in range (1,10):
                second_x = math.cos(second_angle) * (i*20) + 400
                second_y = math.sin(second_angle) * (i*20) + 300
                second_hand = ttk.Label(self.frm, text = self.update_time()["Second"])
                second_hand.place(x=second_x,y=second_y)

            self.c -= 1  # reduce counter
            self.root.after(1000, self.write)  # call again in 1 second

        else:
            self.c = 5   # when counter is 0 reset counter which allows to run infinitely without crashing (while true didn't work)
            self.write()

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
    UTC_clock = Clock("UTC", False)

if __name__ == "__main__":
    main()