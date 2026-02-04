import time
import requests
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.requests import LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data import StockHistoricalDataClient, StockTradesRequest
from datetime import datetime
from alpaca.data.live import StockDataStream
from alpaca.data.requests import StockLatestQuoteRequest


api_KEY = "PKO3W4TBWJ72ZBQF7V7Y5DKBGX"
api_SECRET = "DeyB6e8ZM4Y8tpcsjg3La2ZmqxxTGfyUFN1XdY41FHc2"
lockheed = "LMT"

trading_client = TradingClient(api_KEY , api_SECRET, paper=True) 

positions = trading_client.get_all_positions()
print(positions)

clock = trading_client.get_clock()
print(clock.is_open)

def sell_all_lmt():
    try:
        # Get all open positions
        positions = trading_client.get_all_positions()

        # Find LMT position
        lmt_position = None
        for position in positions:
            if position.symbol == "LMT":
                lmt_position = position
                break

        if lmt_position is None:
            print("No LMT position to sell.")
            return

        qty = int(float(lmt_position.qty))

        # Create sell order
        order = MarketOrderRequest(
            symbol="LMT",
            qty=qty,
            side=OrderSide.SELL,
            time_in_force=TimeInForce.DAY
        )

        trading_client.submit_order(order)
        print(f"Sell order submitted for {qty} shares of LMT")

    except Exception as e:
        print("Error selling LMT:", e)

# Call the function
sell_all_lmt()


# positions = trading_client.get_all_positions()

# for position in positions:
#     print(position.symbol, position.current_price, position.avg_entry_price)

# stream = StockDataStream(api_KEY, api_SECRET)

# async def handle_trade(data):
#     print(data)

# stream.subscribe_trades(handle_trade, "AAPL")

# stream.run()

# market_order_data = MarketOrderRequest(
#     #DIRECT ORDER
#     symbol = "SPY",
#     qty = 1,
#     side = OrderSide.BUY,
#     time_in_force = TimeInForce.DAY
# )

# limit_order_data = LimitOrderRequest(
#     #LIMIT ORDER
#     symbol = "TSLA",
#     qty = 1,
#     side = OrderSide.BUY,
#     time_in_force = TimeInForce.DAY,
#     limit_price = 448.50
# )

# #market_order = trading_client.submit_order(market_order_data)
# limit_order = trading_client.submit_order(limit_order_data)
# print(limit_order)











# print(trading_client.get_account())
# print(f"Account Number : {trading_client.get_account().account_number} ")
# print(f"Cash :  {trading_client.get_account().cash} ")
# print(f"Buying Power :  {trading_client.get_account().buying_power} ")

# data_client = StockHistoricalDataClient(api_KEY , api_SECRET)

# request_parameters =  StockTradesRequest(
#    symbol_or_symbols="AAPL",
#    start=datetime(2025, 1, 14, 14, 30),
#    end=datetime(2025, 1, 14, 14, 45)
# )

# trades = data_client.get_stock_trades(request_parameters)

# print(trades)
# for trade in trades.data["AAPL"]:
#     print(trade)
#     break


# url = "https://paper-api.alpaca.markets/v2/account"
# headers = {
#     "accept": "application/json",
#     "APCA-API-KEY-ID": api_KEY,
#     "APCA-API-SECRET-KEY": api_SECRET
# }
# response = requests.get(url, headers=headers)
# print(response.text)