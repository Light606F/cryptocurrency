from pprint import pprint
from tracemalloc import start
from unicodedata import name
import requests
from pprint import pprint
import asyncio
import websockets
import json
import pandas as pd
import datetime

# mac9wEhZc3qYx9yJ

endpoint = "https://coincheck.com"

async def get_rate():
    rates = pd.Series([],name="rate")
    print(rates)
    # rates = pd.DataFrame(index=[], columns=["rate"])
    while True:
        # time_start = datetime.datetime.now()

        response = requests.get(endpoint + "/api/rate/btc_jpy").json()

        pprint(response)

        rates[datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')] = response["rate"]
        rates.to_pickle('rates.pickle')
        print(rates)

        # time_end = datetime.datetime.now()
        # time_taken = time_end - time_start
        # print(time_taken.total_seconds())
        # print(1-time_taken.total_seconds())

        # if time_taken.seconds >= 1:
        #     print("WARNING: time taken over one second.")

        await asyncio.sleep(1)

async def get_order_books():
    while True:
        # response = requests.get(endpoint + "/api/ticker").json()
        response = requests.get(endpoint + "/api/order_books")

        pprint(response)

        await asyncio.sleep(1)

# get latest trades with websocket
async def get_trades():
    async def get_latest_trade():
        async with websockets.connect("wss://ws-api.coincheck.com/") as websocket:
            await websocket.send(
                json.dumps(
                    {
                        "type": "subscribe", 
                        "channel": "btc_jpy-trades"
                    }
                )
            )
            res = await websocket.recv()
            print(res)

    while True:
        await get_latest_trade()

loop = asyncio.get_event_loop()
loop.create_task(get_trades())
# loop.create_task(get_order_books())
loop.run_until_complete(get_rate())