# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import os
import requests_cache
from pprint import pprint
from datetime import datetime as dt, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData, find_cheapest_flight

requests_cache.install_cache(
    "flight_cache",
    urls_expire_after={
        "*.sheety.co*": requests_cache.DO_NOT_CACHE,
        "*": 3600,
    },
)

data_manager = DataManager()
sheet_data = data_manager.get_destination()
# pprint(sheet_data)

today = dt.now()
tomorrow = today + timedelta(days=1)
six_months_from_today = today + timedelta(days=180)

flight_search = FlightSearch()
flights = flight_search.check_flights(
    origin_city_code="LHR",
    destination_city_code="CDG",
    from_time=tomorrow,
    to_time=six_months_from_today,
)
# pprint(flights)

cheapest_flight = find_cheapest_flight(flights, six_months_from_today.strftime("%Y-%m-%d"))
# pprint(vars(cheapest_flight))
if cheapest_flight.price !="N/A" and cheapest_flight.price < sheet_data[0]["lowestPrice"]:
    pprint(f"Lower price flight found to {sheet_data[0]['city']}!")
    data_manager.update_lower_price(sheet_data[0]["id"], cheapest_flight.price)
