# Kagami - Main UI Script
#
# Written by Martianmellow12
from tkinter import font
import tkinter as tk


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
root.geometry("350x200")
root.configure(bg="#ffffff")


#######################
# Font Configurations #
#######################
# Scalar: 1.25 * fontsize

SIZE_LARGE = {
    "font":font.Font(family="Consolas", size=64),
    "scale":80
}

SIZE_MEDIUM = {
    "font":font.Font(family="Consolas", size=32),
    "scale":40
}


####################
# Text Item Widget #
####################
class TextItem(tk.Frame):

    def __init__(self, parent, size):
        # Set instance variables
        self.parent = parent
        self.size = size
        self.hidden = False
        self.blinking = False
        self.blink_interval = 1000
        self.blink_low = (170, 170, 170)

        # Configure widgets
        tk.Frame.__init__(self, parent, borderwidth=0, highlightthickness=0)
        self.c = tk.Canvas(self, bg="#000000", height=self.size["scale"], borderwidth=0, highlightthickness=0)
        self.c_text = self.c.create_text(0, 0, text="Hello!", fill="#ffffff", anchor="nw", font=self.size["font"])
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

        # Configure widgets
        tk.Frame.__init__(self, parent, borderwidth=0, highlightthickness=0)
        self.c = tk.Canvas(self, bg="#000000", height=15, borderwidth=0, highlightthickness=0)
        self.c_line = self.c.create_rectangle(1, 10, self.width, 14, fill="#ffffff")
        self.c.pack(side="top", fill="x")


#########################
# Widget Configurations #
#########################

test1 = TextItem(root, SIZE_LARGE)
test2 = TextItem(root, SIZE_MEDIUM)
test3 = Divider(root, 300)
test1.grid(row=0, column=0)
test2.grid(row=2, column=0)
test3.grid(row=1, column=0)

# Main loop
root.after(3000, lambda: test2.blink(True))
root.after(3250, lambda: test1.blink(True))
root.mainloop()
