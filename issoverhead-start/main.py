import requests
from datetime import datetime

MY_LAT = 41.878113 # Your latitude
MY_LONG = -87.629799 # Your longitude

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.
def iss_is_close():
    close_lat = MY_LAT - 5 <= iss_latitude <= MY_LAT + 5
    close_long = MY_LONG - 5 <= iss_longitude <= MY_LONG + 5
    return close_lat and close_long


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()

def is_dark():
    if time_now.hour >= sunset or time_now.hour <= sunrise:
        return True
    else:
        return False
#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.



