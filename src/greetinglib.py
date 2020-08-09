# Kagami - Greeting Generator Library
#
# Written by Martianmellow12
import datetime

######################
# Greeting Generator #
######################
def get_greeting():
    n = datetime.datetime.now()

    # Holiday Greetings
    if n.month==12 and n.day==25: return "Merry Christmas!"
    if n.month==10 and n.day==31: return "Happy Halloween!"
    if n.month==1 and n.day==1: return "Happy New Year's!"

    # Default Greetings
    if n.hour in range(0, 12): return "Good Morning"
    if n.hour in range(12, 18): return "Good Afternoon"
    if n.hour in range(18, 24): return "Good Evening"
