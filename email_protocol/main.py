import random
import smtplib
import datetime as dt
import os

MY_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("MY_PASSWORD")

now = dt.datetime.now()
weekday = now.weekday()
if weekday == 6:
    with open("quotes.txt", "r", encoding="utf-8") as file:
        quotes = file.readlines()
    random_quote = random.choice(quotes)
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs="taylorgibson@msn.com",
                            msg=f"Subject:Your Weekly Motivational Quote\n\n{random_quote}"
        )
