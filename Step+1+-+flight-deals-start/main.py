from pprint import pprint
from datetime import datetime as dt, timedelta
import requests_cache
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

requests_cache.install_cache(
    "flight_cache",
    urls_expire_after={
        "*.sheety.co*": requests_cache.DO_NOT_CACHE,
        "*.callmebot.com*": requests_cache.DO_NOT_CACHE,
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
notification_manager = NotificationManager()

for row in sheet_data:
    print(f"Checking for flights to {row['city']}")
    flights = flight_search.check_flights(
        origin_city_code="ORD",
        destination_city_code=row["iataCode"],
        from_time=tomorrow,
        to_time=six_months_from_today,
        is_direct=True,
    )
    cheapest_flight = find_cheapest_flight(
        flights, six_months_from_today.strftime("%Y-%m-%d")
    )

    if cheapest_flight.price == "N/A":
        print(f"No direct flights to {row['city']}, checking with a layover...")
        flights = flight_search.check_flights(
            origin_city_code="ORD",
            destination_city_code=row["iataCode"],
            from_time=tomorrow,
            to_time=six_months_from_today,
            is_direct=False,
        )
        cheapest_flight = find_cheapest_flight(
            flights, six_months_from_today.strftime("%Y-%m-%d")
        )

    pprint(f"{row['city']}: USD {cheapest_flight.price}")
    if cheapest_flight.price != "N/A" and cheapest_flight.price < row["lowestPrice"]:
        stops = cheapest_flight.stops
        stop_text = "nonstop" if stops == 0 else f"{stops} stop(s)"
        print(f"Lower price flight found to {row['iataCode']}")
        data_manager.update_lower_price(row["id"], cheapest_flight.price)
        notification_manager.send_message(
            f"Low price alert! {row['city']}: USD ${cheapest_flight.price} ({stop_text})"
        )
# pprint(flights)
