import os
import requests
from dotenv import load_dotenv

load_dotenv()


class DataManager:
    """Talks to the Sheety API to get city code and pricing information from the Google Sheet"""

    def __init__(self):
        self.sheety_endpoint = os.environ["SHEETY_ENDPOINT"]
        self.sheety_auth = (
            os.environ["SHEETY_USERNAME"],
            os.environ["SHEETY_PASSWORD"],
        )
        self.destination_data = {}

    def get_destination(self):
        """Fetches the destination rows from the Sheety sheet and returns them as a list of dicts"""
        response = requests.get(
            url=self.sheety_endpoint,
            auth=self.sheety_auth,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_lower_price(self, row_id, new_price):

        new_data = {
            "price": {
                "lowestPrice": new_price
            }
        }

        requests.put(
            url=f"{self.sheety_endpoint}/{row_id}",
            json=new_data,
            auth=self.sheety_auth,
            timeout = 60,
        )
