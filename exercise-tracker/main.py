import os
import requests
import requests_cache
from datetime import datetime

# Source - https://stackoverflow.com/a/58055668
# Posted by Zhe, modified by community. See post 'Timeline' for change history
# Retrieved 2026-08-30, License - CC BY-SA 4.0

import requests


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


exercise_text = input("Describe your exercise: ")

headers = {
    "Content-Type": "application/json",
    "x-app-id": "app_1d05767a065c496dbebefa1c",
    "x-app-key": "nix_live_u7xHEPxpSgX4LM2BLJ8hxPpCMDxkO9sy",
}

requests_cache.install_cache("exercise_cache", expire_after=300)

api_endpoint = "https://app.100daysofpython.dev"

body = {
    "query": exercise_text,
}

response = requests.post(
    f"{api_endpoint}/v1/nutrition/natural/exercise",
    headers=headers,
    json=body,
    timeout=30,
)
response.raise_for_status()

sheet_endpoint = (
    "https://api.sheety.co/87bb6c7260f0526b2085824fded11c75/exerciseTracker/workouts"
)

exercise_data = response.json()
# print(exercise_data)

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercises in exercise_data["exercises"]:
    sheet_body = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercises["name"].title(),
            "duration": exercises["duration_min"],
            "calories": exercises["nf_calories"],
        }
    }
    sheet_response = requests.post(
        sheet_endpoint,
        json=sheet_body,
        headers={"Content-Type": "application/json"},
        auth=BearerAuth("adsfavhadsjkfduoiupoaaaaadfjkelkankjchvdk"),
        timeout=30,
    )
    print(sheet_response.text)
