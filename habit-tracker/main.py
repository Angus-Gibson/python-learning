import requests
import os
from datetime import datetime

pixela_endpoint = "https://pixe.la/v1/users"

MY_TOKEN = os.environ.get("my_token")
USERNAME = os.environ.get("username")

user_params = {
   "token": MY_TOKEN,
   "username": USERNAME,
   "agreeTermsOfService": "yes",
   "notMinor": "yes"
}

# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_config = {
    "id": "primarygraph",
    "name": "Coding Graph",
    "unit": "day",
    "type": "int",
    "color": "shibafu",
}

headers = {
    "X-USER-TOKEN": MY_TOKEN
}

# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(response.text)

pixela_pixel_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/primarygraph"

today = datetime.now()

pixel_config = {
    "date": today.strftime("%Y%m%d"),
    "quantity": "1"
}

response = requests.post(url=pixela_pixel_endpoint, json=pixel_config, headers=headers)
print(response.text)

new_config = {
    "timezone": "America/Chicago",
    "description": "Each day is a completed lesson of 100 Days of Python Code (beginning from Day 37)"
}

# response = requests.put(url=pixela_pixel_endpoint, json=new_config, headers=headers)
# print(response.text)

# delete_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/primarygraph/{today.strftime('%Y%m%d')}"
# response = requests.delete(url=delete_endpoint, headers=headers)
# print(response.text)

