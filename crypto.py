import smtplib
import requests
from selenium import webdriver
from datetime import datetime, timedelta

BTC = "BTC"
NEWS_KEYWORD = "Bitcoin"

CRYPTO_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

CRYPTO_API = "CRYPTO API"
NEWS_API = "NEWS API"

chrome_driver_path = "/Applications/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

crypto_parameters = {
    "function": "DIGITAL_CURRENCY_DAILY",
    "symbol": BTC,
    "market": "USD",
    "apikey": CRYPTO_API,
}

response = requests.get(CRYPTO_ENDPOINT, params=crypto_parameters)
data = response.json()

date = datetime.today()
current_date = date.strftime("%Y-%m-%d")
day_2 = date - timedelta(days=1)
day_before = day_2.strftime("%Y-%m-%d")

data_list = [value for (key, value) in data.items()]
yesterday = data_list[1][day_before]
yesterday_closing = float(yesterday["4a. close (USD)"])

driver.get("https://www.coindesk.com/price/bitcoin")
current_price = driver.find_element_by_css_selector("div .price-large").text
returned_price = current_price.split('$')[1]
driver.close()


today = datetime.utcnow().date()
today_day = int(datetime.now().strftime("%d"))


def get_news_email():
    global yesterday_closing, returned_price, today_day
    news_params = {
        "apiKey": NEWS_API,
        "qInTitle": NEWS_KEYWORD
    }
    news = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news.json()["articles"]
    formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in
                          articles if today_day - int(article['publishedAt'].split("T")[0].split("-")[2]) <= 2 or today_day - int(article['publishedAt'].split("T")[0].split("-")[2]) <= -26]
    for article in formatted_articles:
        my_email = "EMAIL ADDRESS"
        password = "PASSWORD"
        message = f"Subject: Bitcoin News Today\n\nYesterday's closing price: {yesterday_closing}\nCurrent Bitcoin " \
                  f"price: {returned_price}\n\n{article} "
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(my_email, password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg=message.encode("utf8"),
            )


get_news_email()
