import requests
import os
from dotenv import load_dotenv
class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        load_dotenv()
        self.sheety_endpoint = os.getenv("SHEETY_ENDPOINT")
        self.sheety_auth = (os.getenv("SHEETY_USERNAME"),
                            os.getenv("SHEETY_PASSWORD"),
        )
        
        response = requests.get(url=self.sheety_endpoint,
                                auth=self.sheety_auth,
                                timeout=10,
        )
        response.raise_for_status()
        self.data = response.json()