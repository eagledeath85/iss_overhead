import requests
from datetime import datetime

MY_LAT = 32.076102
MY_LNG = 34.851810
URL = "https://api.sunrise-sunset.org/json"
parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0,
}

# Send get request to the API and save the response
response = requests.get(url=URL, params=parameters)
response.raise_for_status()

# Parse the response in JSON format
data = response.json()

# Get sunrise and sunset time from data
sunrise = data["results"]["sunrise"]
sunset = data["results"]["sunset"]

print(sunrise)

# Get current time
time_now = datetime.now()
print(time_now)

# Isolate the HH from sunrise time
sunrise_hour = sunrise.split("T")[1].split(":")[0]
print(sunrise_hour)