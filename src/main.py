# Kagami - Main UI Script
#
# Written by Martianmellow12
from tkinter import font
import tkinter as tk
import math
import datetime

# Kagami Libraries
import greetinglib
import weatherlib


###########################
# Configuration Constants #
###########################
FULLSCREEN = False  # Controls whether or not the window is fullscreen
LAYOUT_BG = False   # Sets the bg color of the window to help make grid cells visible when changing the layout


##########################
# Color Helper Functions #
##########################
def hexToRGB(hexstr):
    # Assumes hexstr is in the format "#xxxxxx"
    rgb_value = (
        int(hexstr[1:3], 16),
        int(hexstr[3:5], 16),
        int(hexstr[5:7], 16)
    )
    return rgb_value

def RGBToHex(rgb_value):
    # Value returned is in the format "#xxxxxx"
    return f"#{hex(rgb_value[0])[2:4].rjust(2, '0')}{hex(rgb_value[1])[2:4].rjust(2, '0')}{hex(rgb_value[2])[2:4].rjust(2, '0')}"


#####################
# Root Window Setup #
#####################

# Configure basic attributes
root = tk.Tk()
root.title("Kagami - Test")

if FULLSCREEN: root.attributes("-fullscreen", True)
else: root.geometry("1000x800")

if LAYOUT_BG: root.configure(bg="#ffffff")
else: root.configure(bg="#000000")


#######################
# Font Configurations #
#######################
# Scalar: 1.5625 * fontsize

CONSOLAS_LARGE = {
    "font":font.Font(family="Consolas", size=64),
    "scale":100
}

CONSOLAS_MEDIUM = {
    "font":font.Font(family="Consolas", size=32),
    "scale":50
}

BAHNS_LARGE = {
    "font":font.Font(family="Bahnschrift", size=64),
    "scale":100
}

BAHNS_MEDIUM = {
    "font":font.Font(family="Bahnschrift", size=32),
    "scale":50
}


####################
# Text Item Widget #
####################
class TextItem(tk.Frame):

    def __init__(self, parent, text, size, width):
        # Set instance variables
        self.parent = parent
        self.size = size
        self.hidden = False
        self.blinking = False
        self.blink_interval = 1000
        self.blink_low = (170, 170, 170)

        # Configure widgets
        tk.Frame.__init__(self, parent, borderwidth=0, highlightthickness=0)
        self.c = tk.Canvas(self, bg="#000000", height=self.size["scale"], borderwidth=0, highlightthickness=0, width=width)
        self.c_text = self.c.create_text(0, 0, text=text, fill="#ffffff", anchor="nw", font=self.size["font"])
        self.c.pack(side="top", fill="x")

    def __getcolor__(self):
        return hexToRGB(self.c.itemcget(self.c_text, 'fill'))

    def __setcolor__(self, rgb_color):
        self.c.itemconfigure(self.c_text, fill=RGBToHex((rgb_color[0], rgb_color[1], rgb_color[2])))

    def __hider__(self):
        ccolor = self.__getcolor__()

        # Unhiding
        if self.hidden==False and ccolor!=(255, 255, 255):
            self.__setcolor__((ccolor[0]+3, ccolor[1]+3, ccolor[2]+3))
            self.parent.after(4, self.__hider__)

        # Hiding
        if self.hidden==True and ccolor!=(0, 0, 0):
            self.__setcolor__((ccolor[0]-3, ccolor[1]-3, ccolor[2]-3))
            self.parent.after(4, self.__hider__)

    def __blinker__(self):
        if not self.blinking: return
        if self.hidden: return

        # High to low
        if (self.__getcolor__() == (255, 255, 255)):
            self.__setcolor__(self.blink_low)
            self.parent.after(int(self.blink_interval/2), self.__blinker__)

        # Low to high
        else:
            self.__setcolor__((255, 255, 255))
            self.parent.after(int(self.blink_interval/2), self.__blinker__)

    def set(self, text):
        self.c.itemconfigure(self.c_text, text=text)

    def hide(self, hide_text):
        # Disable other text effects
        self.blinking = False

        # Hide the text
        self.hidden = hide_text
        self.__hider__()

    def blink(self, blink_text, interval=1000):
        # Set the text to blinking
        self.blinking = blink_text
        self.blink_interval = interval
        self.__blinker__()

    def test(self):
        pass


##################
# Divider Widget #
##################
class Divider(tk.Frame):

    def __init__(self, parent, width):
        # Set instance variables
        self.parent = parent
        self.width = width
        self.hidden = False
        self.hide_step = 0      # Max step is 90

        # Constants
        self.max_step = 180
        self.step_speed = 5

        # Configure widgets
        tk.Frame.__init__(self, parent, borderwidth=0, highlightthickness=0)
        self.c = tk.Canvas(self, bg="#000000", height=15, borderwidth=0, highlightthickness=0, width=width)
        self.c_line = self.c.create_rectangle(1, 5, self.width, 9, fill="#ffffff")
        self.c.pack(side="top", fill="x")

    def __setwidth__(self, width):
        self.c.coords(self.c_line, 1, 5, width, 9)

    def __getstepwidth__(self, step):
        return math.cos((step * (math.pi/180)) + math.pi) * (self.width/2) + (self.width/2)

    def __hider__(self):
        # Unhiding
        if self.hidden==False and self.hide_step<self.max_step:
            self.__setwidth__(self.__getstepwidth__(self.hide_step))
            self.hide_step += 1
            self.parent.after(self.step_speed, self.__hider__)

        # Hiding
        if self.hidden==True and self.hide_step>0:
            self.__setwidth__(self.__getstepwidth__(self.hide_step))
            self.hide_step -= 1
            self.parent.after(self.step_speed, self.__hider__)


    def hide(self, hide_div):
        self.hidden = hide_div
        self.hide_step = self.max_step if hide_div else 0
        self.__hider__()


########################
# Date and Time Widget #
########################
class DateAndTime(TextItem):

    def __init__(self, parent, size, width):
        # Set instance variables
        self.parent = parent
        self.size = size
        self.width = width

        # Configure widgets
        TextItem.__init__(self, self.parent, "[BLANK]", self.size, self.width)

        # Start the time updater
        self.__updater__()

    def __updater__(self):
        now = datetime.datetime.now()
        self.set(now.strftime("%B %d, %Y\t%I:%M:%S%p"))
        self.parent.after(1000, self.__updater__)


#########################
# Widget Configurations #
#########################

greeting = TextItem(root, "[BLANK]", CONSOLAS_LARGE, 800)
date_and_time = DateAndTime(root, BAHNS_MEDIUM, 800)
div1 = Divider(root, 700)
weather_temp = TextItem(root, "[BLANK]", CONSOLAS_MEDIUM, 800)
weather_type = TextItem(root, "[BLANK]", CONSOLAS_MEDIUM, 800)
greeting.grid(row=0, column=0, sticky="w")          # Greeting text
div1.grid(row=1, column=0, sticky="w")              # Divider between the greeting and date/time
date_and_time.grid(row=2, column=0, sticky="w")     # Date and time text
root.grid_rowconfigure(3, minsize=75)               # Pad the space between the date/time and weather
weather_temp.grid(row=4, column=0, sticky="w")      # Weather temperature text
weather_type.grid(row=5, column=0, sticky="w")      # Weather type text



########################################
# Activation and Deactivation Routines #
########################################
def activate(window):
    greeting.set(greetinglib.get_greeting())
    weather_temp.set(weatherlib.get_tempstr(weatherlib.CITY_RALEIGH))
    weather_type.set(weatherlib.get_typestr(weatherlib.CITY_RALEIGH))
    window.after(500, lambda:greeting.hide(False))
    window.after(0, lambda:div1.hide(False))
    window.after(600, lambda:date_and_time.hide(False))
    window.after(700, lambda:weather_temp.hide(False))
    window.after(800, lambda:weather_type.hide(False))


def deactivate(window):
    window.after(0, lambda:greeting.hide(True))
    window.after(500, lambda:div1.hide(True))
    window.after(100, lambda:date_and_time.hide(True))
    window.after(200, lambda:weather_temp.hide(True))
    window.after(300, lambda:weather_type.hide(True))


#############
# Main loop #
#############
deactivate(root)
root.after(2000, lambda:activate(root))
root.mainloop()
