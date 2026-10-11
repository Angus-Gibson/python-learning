# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import os
from pprint import pprint
from data_manager import DataManager

data_manager = DataManager()
sheet_data = data_manager.get_destination()
pprint(sheet_data)
