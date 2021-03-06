# Kagami - Weather Library
#
# Written by Martianmellow12

###########################################
# Weather Data is from openweathermap.org #
###########################################

import requests
import time

# API Key - REMOVE BEFORE COMMITS!!!
API_KEY = ""


####################################
# Open Weather Map Condition Codes #
####################################
OWM_CONDITION_CODES = {
    # Group 2xx: Thunderstorm
    200: "Thunderstorm (Light Rain)",
    201: "Thunderstorm (Rain)",
    202: "Thunderstorm (Heavy Rain)",
    210: "Light Thunderstorm",
    211: "Thunderstorm",
    212: "Heavy Thunderstorm",
    221: "Ragged Thunderstorm",
    230: "Thunderstorm (Light Drizzle)",
    231: "Thunderstorm (Drizzle)",
    232: "Thunderstorm (Heavy Drizzle)",

    # Group 3xx: Drizzle
    300: "Light Drizzle",
    301: "Drizzle",
    302: "Heavy Drizzle",
    310: "Light Drizzle Rain",
    311: "Drizzle Rain",
    312: "Heavy Drizzle Rain",
    313: "Shower Rain and Drizzle",
    314: "Heavy Shower Rain and Drizzle",
    321: "Shower Drizzle",

    # Group 5xx: Rain
    500: "Light Rain",
    501: "Moderate Rain",
    502: "Heavy Rain",
    503: "Very Heavy Rain",
    504: "Extreme Rain",
    511: "Freezing Rain",
    520: "Light Shower Rain",
    521: "Shower Rain",
    522: "Heavy Shower Rain",
    531: "Ragged Shower Rain",

    # Group 6xx: Snow
    600: "Light Snow",
    601: "Snow",
    602: "Heavy Snow",
    611: "Sleet",
    612: "Light Shower Sleet",
    613: "Shower Sleet",
    615: "Light Rain and Snow",
    616: "Rain and Snow",
    620: "Light Shower Snow",
    621: "Shower Snow",
    622: "Heavy Shower Snow",

    # Group 7xx: Atmosphere
    701: "Mist",
    711: "Smoke",
    721: "Haze",
    731: "Dust Whirls",
    741: "Fog",
    751: "Sand",
    761: "Dust",
    762: "Ash",
    771: "Squall",
    781: "Tornado",

    # Group 800: Clear
    800: "Clear",

    # Group 8xx: Clouds
    801: "Slightly Cloudy",
    802: "Partly Cloudy",
    803: "Cloudy",
    804: "Overcast"
}


#########################
# Weather API Functions #
#########################
CITY_RALEIGH = ("35.769375", "-78.674016")    # My home city's latitude and longitude :D

# Make an API Call for a specific city
def __apicallOLD__(api_key, city_id):
    URL = f"https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}"
    return requests.get(URL).json()

# Make an API call for a given longitude/latitude pair
def __apicall__(api_key, latlong_tuple):
    URL = f"https://api.openweathermap.org/data/2.5/onecall?lat={latlong_tuple[0]}&lon={latlong_tuple[1]}&exclude=daily,minutely&appid={api_key}"
    return requests.get(URL).json()

# Convert Kelvin to degrees Fahrenheit
def __ktof__(kelvin_temp):
    return ((kelvin_temp - 273.15)*9)/5 + 32

# Get a string describing the temperature
def get_tempstr(latlong_tuple):
    global API_KEY

    # Make the API call
    results = __apicall__(API_KEY, latlong_tuple)

    # Make sure the call was successful
    if "cod" in results.keys() and results["cod"] != 200: return "<ERR: Unable to get temperature data>"
    else: return f"{int(__ktof__(results['current']['temp']))}°F (feels like {int(__ktof__(results['current']['feels_like']))}°F)"

# Get a string describing the weather weather type
def get_typestr(latlong_tuple):
    global API_KEY

    # Make the API call
    results = __apicall__(API_KEY, latlong_tuple)

    # Make sure the call was successful
    if "cod" in results.keys() and results["cod"] != 200: return "<ERR: Unable to get weather data>"
    else:
        resultstr = "/"
        for i in results["current"]["weather"]:
            resultstr += OWM_CONDITION_CODES[i["id"]]+"/"
        return resultstr

# Check if a raincoat is recommended (uses next 12 hours)
def get_raincoat_rec(latlong_tuple):
    global API_KEY

    # Make the API call
    results = __apicall__(API_KEY, latlong_tuple)

    # Extract the results
    if "cod" in results.keys() and results["cod"] != 200: return None
    else:
        recommended = False
        for i in results["hourly"]:
            for j in i["weather"]:
                if j["id"]==500 and (time.time()+43200)>i["dt"]: recommended = True
        return recommended
