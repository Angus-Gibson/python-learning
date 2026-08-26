import os

import requests
from twilio.rest import Client

# MY_LAT = 41.878113
# MY_LONG = -87.629799

MY_LAT = 24.7
MY_LONG = 134.22

ACCOUNT_SID = os.environ.get("TWILIO_SID")
AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
MY_PHONE = os.environ.get("MY_PHONE")
TWILIO_PHONE = os.environ.get("TWILIO_PHONE")
CONTENT_SID = os.environ.get("CONTENT_SID")

OWM_API_KEY = os.environ.get("OWM_API_KEY")
parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": OWM_API_KEY,
    "units": "imperial",
    "cnt": 4,
}

response = requests.get(
    "https://api.openweathermap.org/data/2.5/forecast",
    params=parameters,
    timeout=10,
)
response.raise_for_status()
data = response.json()

for forecast in data["list"]:
    if forecast["weather"][0]["id"] < 700:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            to=f"whatsapp:{MY_PHONE}",
            from_=f"whatsapp:{TWILIO_PHONE}",
            content_sid=CONTENT_SID,
        )

        print(message.status)
        break
