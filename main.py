############################ RESPONSE CODES ############################

# 1XX: Hold On, something's happening, this is not final
# 2XX: Here You Go, you should receive the data you're expecting
# 3XX: Go Away, you don't have permission to get this thing
# 4XX: You Screwed Up
# 5XX: I, the server, Screwed Up

import requests

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()

# Get the response on JSON format
data = response.json()

longitude = data["iss_position"]["longitude"]
latitude = data["iss_position"]["latitude"]

iss_position = (longitude, latitude)

print(iss_position)