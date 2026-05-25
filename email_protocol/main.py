# import smtplib

# my_email = "angusgibsonpython@gmail.com"
# password = "zubyeifsrqgirwae"

# with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
#     connection.starttls()
#     connection.login(user=my_email, password=password)
#     connection.sendmail(from_addr=my_email,
#                         to_addrs="angusgibsonpython@yahoo.com",
#                         msg="Subject:Hello\n\nThis is the body of the email."
#     )

# import datetime as dt

# now = dt.datetime.now()
# year = now.year
# weekday = now.weekday()
# print(weekday)

# date_of_birth = dt.datetime(year=1990, month=1, day=14, hour=3)
# print(date_of_birth)
import random
import smtplib
import datetime as dt

MY_EMAIL = "angusgibsonpython@gmail.com"
PASSWORD = "zubyeifsrqgirwae"

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
