import requests
from twilio.rest import Client
import os

# MY_LAT = 41.878113
# MY_LONG = -87.629799

MY_LAT = 24.7
MY_LONG = 134.22

account_sid = "REDACTED_TWILIO_SID"
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

OWM_API_KEY = os.environ.get("OWM_API_KEY")
parameters = {

    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": OWM_API_KEY,
    "units": "imperial",
    "cnt": 4,
}

response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()
data = response.json()

for forecast in data["list"]:
    if forecast["weather"][0]["id"] < 700:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to=f"whatsapp:{os.environ.get('MY_PHONE_NUMBER')}",
            from_="whatsapp:+17372583478",
            content_sid="HXfe5ab5f00277942d4d4200328b4d403c",
        )

        print(message.status)   
        break
