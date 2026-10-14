import os
import smtplib
import requests


class NotificationManager:
    """Sends a notification via CallMeBot API call to a WhatsApp Number"""

    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.callmebot_endpoint = os.environ["CALLMEBOT_ENDPOINT"]
        self.phone = os.environ["PHONE_NUMBER"]
        self.apikey = os.environ["CALLMEBOT_API_KEY"]
        self.email = os.environ["EMAIL_ADDRESS"]
        self.smtp_address = os.environ["SMTP_ADDRESS"]
        self.smtp_password = os.environ["SMTP_PASSWORD"]

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

    def send_email(self, recipient, message):
        """Sends e-mail to subscribers to flight club."""
        with smtplib.SMTP(self.smtp_address, port=587) as connection:
            connection.starttls()
            connection.login(user=self.email, password=self.smtp_password)
            connection.sendmail(
                from_addr=self.email,
                to_addrs=recipient,
                msg=f"Subject: Low Price Alert!\n\n{message}".encode("utf-8"),
            )
