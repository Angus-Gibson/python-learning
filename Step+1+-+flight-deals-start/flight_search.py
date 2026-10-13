import os
import requests
from dotenv import load_dotenv

load_dotenv()

class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self._api_key = os.environ["SERP_API_KEY"]
        self.endpoint = "https://serpapi.com/search"
        self.params = {
            "engine": "google_flights",
            "type": "1",
            "adults": "1",
            "currency": "USD",
            "api_key": self._api_key,
        }

    def check_flights(
        self,
        origin_city_code,
        destination_city_code,
        from_time,
        to_time,
        is_direct=True,
    ):
        """Returns JSON of flight info & pricing from input departure/destination city codes, departure & return dates, # of adults traveling"""
        if is_direct:
            self.params["outbound_date"] = from_time.strftime("%Y-%m-%d")
            self.params["return_date"] = to_time.strftime("%Y-%m-%d")
            self.params["departure_id"] = origin_city_code
            self.params["arrival_id"] = destination_city_code
            self.params["stops"] = 1
            response = requests.get(url=self.endpoint, params=self.params, timeout=60)
            response.raise_for_status()
            flight_data = response.json()

        else:
            self.params["outbound_date"] = from_time.strftime("%Y-%m-%d")
            self.params["return_date"] = to_time.strftime("%Y-%m-%d")
            self.params["departure_id"] = origin_city_code
            self.params["arrival_id"] = destination_city_code
            self.params["stops"] = 2
            response = requests.get(url=self.endpoint, params=self.params, timeout=60)
            response.raise_for_status()
            flight_data = response.json()

        return flight_data
