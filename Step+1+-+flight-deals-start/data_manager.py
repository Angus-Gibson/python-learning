import requests
import os
from dotenv import load_dotenv
class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        load_dotenv()
    print(os.getenv("SHEETY_ENDPOINT"))
        # self.sheety_endpoint = os.getenv("SHEETY_ENDPOINT")
        # self.sheety_headers = {
        #     "Authorization": f"Basic {os.getenv('YOUR_BEARER_TOKEN')}",
        #     "Content-Type": "application/json"
        # }
        # self.sheety_auth = (os.getenv("SHEETY_USERNAME"), os.getenv("SHEETY_PASSWORD"))
        
        # response = requests.get(url=self.sheety_endpoint, headers=self.sheety_headers, params=self.params, timeout=10)
        # self.data = response.json()