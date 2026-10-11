# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import os
import requests_cache
from pprint import pprint
from datetime import datetime as dt, timedelta
from data_manager import DataManager
from flight_search import FlightSearch

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
tomorrow_str = tomorrow.strftime("%Y-%m-%d")
six_months_str = six_months_from_today.strftime("%Y-%m-%d")
today_str = today.strftime("%Y-%m-%d")

flight_search = FlightSearch()
search = flight_search.check_flights(
    origin_city_code="LHR",
    destination_city_code="CDG",
    from_time=today_str,
    to_time=tomorrow_str,
)
pprint(search)
