#Import requirements
import time
import json
import requests
from kafka import KafkaProducer

#Define variables for API
API_KEY="d76lo4pr01qtg3ne2jf0d76lo4pr01qtg3ne2jfg"
BASE_URL = "https://finnhub.io/api/v1/quote"
SYMBOLS = ["AAPL", "MSFT", "TSLA", "GOOGL", "AMZN"] #List of company symbols to fetch quotes for

#Initial Producer
producer = KafkaProducer (
    bootstrap_servers=["localhost:29092"], 
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

#Retrive Data
#The fetch_quote function takes a stock symbol as input, constructs the API URL, and makes a GET request to fetch the stock quote. It handles any exceptions that may occur during the request and returns the quote data as a dictionary, including the symbol and the timestamp of when the data was fetched.
def fetch_quote(symbol):
    url = f"{BASE_URL}?symbol={symbol}&token={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        data["symbol"] = symbol
        data["fetched_at"] = int (time.time())
        return data
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

#Looping and Pushing to Stream 
#making an infinite loop to continuously fetch and produce stock quotes every 6 seconds. Each quote is sent to the "stock-quotes" topic in Kafka.
while True:
    for symbol in SYMBOLS:
        quote = fetch_quote(symbol)
        if quote:
            print(f"Producing: {quote}")
            producer.send("stock-quotes", value=quote)
    time.sleep(6)