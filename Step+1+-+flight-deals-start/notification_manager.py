import os
import requests


class NotificationManager:
    """Sends a notification via CallMeBot API call to a WhatsApp Number"""

    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.callmebot_endpoint = os.environ["CALLMEBOT_ENDPOINT"]
        self.phone = os.environ["PHONE_NUMBER"]
        self.apikey = os.environ["CALLMEBOT_API_KEY"]

    def send_message(self, message):
        """Sends Whatsapp text  via CallMeBot API call"""
        url = self.callmebot_endpoint
        params = {
            "phone": self.phone,
            "text": message,
            "apikey": self.apikey,
        }
        response = requests.get(url, params=params, timeout=90)
        response.raise_for_status()
        print(response.text)
