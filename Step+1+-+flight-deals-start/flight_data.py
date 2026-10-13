class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(
        self, price, origin_airport, destination_airport, out_date, return_date
    ):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date


def find_cheapest_flight(data, return_date):

    if data is None:
        print("No flight data")
        return FlightData("N/A", "N/A", "(N/A)", "(N/A)", "(N/A)")

    all_flights = data.get("best_flights", []) + data.get("other_flights", [])

    if not all_flights:
        print("No flights found for this route.")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")

    first_flight = all_flights[0]
    lowest_price = first_flight["price"]
    origin = first_flight["flights"][0]["departure_airport"]["id"]
    destination = first_flight["flights"][-1]["arrival_airport"]["id"]
    out_date = first_flight["flights"][0]["departure_airport"]["time"].split(" ")[0]

    cheapest_flight = FlightData(
        lowest_price, origin, destination, out_date, return_date
    )

    for flight in all_flights:
        try:
            price = flight["price"]
        except KeyError:
            print("--- No price available for this flight. ---")
            continue
        if price < lowest_price:
            lowest_price = price
            origin = flight["flights"][0]["departure_airport"]["id"]
            destination = flight["flights"][-1]["arrival_airport"]["id"]
            out_date = flight["flights"][0]["departure_airport"]["time"].split(" ")[0]
            cheapest_flight = FlightData(
                lowest_price, origin, destination, out_date, return_date
            )
            print(f"Lowest price to {destination} is USD {lowest_price}")

    return cheapest_flight
