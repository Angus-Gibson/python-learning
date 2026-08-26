import requests
import requests_cache
import os
from twilio.rest import Client
from newsapi import NewsApiClient

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API = os.environ.get("STOCK_API")
NEWS_API = os.environ.get("NEWS_API")
ACCOUNT_SID = os.environ.get("TWILIO_SID")
AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
requests_cache.install_cache("stock_news_cache", expire_after=3600)  # Cache for 1 hour
URL = (
    "https://www.alphavantage.co/query?"
    f"function=TIME_SERIES_DAILY&symbol={STOCK}"
    f"&interval=5min&apikey={STOCK_API}"
)
r = requests.get(URL, timeout=10)
r.raise_for_status()
data = r.json()

# print(data)

time_series = data["Time Series (Daily)"]
dates = list(time_series)

for index in range(len(dates) - 1):
    yesterday_close = float(time_series[dates[index]]["4. close"])
    today_close = float(time_series[dates[index + 1]]["4. close"])
    change = (today_close - yesterday_close) / yesterday_close * 100
    if abs(change) >= 5:
        # print("Get News")
        newsapi = NewsApiClient(api_key=f"{NEWS_API}")
        news = newsapi.get_everything(
            q=f"{COMPANY_NAME}", language="en", sort_by="relevancy", page_size=3
        )
        articles = news["articles"]
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            to="whatsapp:+14238342300",
            from_="whatsapp:+17372583478",
            content_sid="HX7cf5a23fe00549e2ed931e272889fb49",
        )
## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
