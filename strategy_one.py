from datetime import datetime
import time
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import OrderStatus

#API KEY and API SECRET change depending on which account to use

api_KEY = "REDACTED" #Specific to an account
api_SECRET = "REDACTED" #Specific to an account
stock_symbol = "LMT"

trading_client = TradingClient(api_KEY , api_SECRET, paper=True) 
data_client = StockHistoricalDataClient(api_KEY, api_SECRET)

#ACCOUNT DATA

account_data = trading_client.get_account()
cash_available = float(account_data.cash)
print(f"Cash Available: ${cash_available}")

#Checking if Market is OPEN
#IF Market is CLOSED, wait until market is OPEN to execute trades

clock = trading_client.get_clock()

if not clock.is_open:
    time_until_open = (clock.next_open - datetime.utcnow()).total_seconds()
    print(f"Market is CLOSED. Sleeping for {int(time_until_open)} seconds.")
    time.sleep(max(time_until_open, 0))
else:
    print("Market is OPEN")

#COLLECTING STOCK PRICE and determing amount of shares to BUY

quote_request = StockLatestQuoteRequest(symbol_or_symbols=stock_symbol)
quote = data_client.get_stock_latest_quote(quote_request)[stock_symbol]
price = float(quote.ask_price or quote.bid_price)  
print(f"{stock_symbol} price: ${price:.2f}")


qty_to_buy = int(cash_available // (price))
if qty_to_buy <= 0:
    raise Exception("You are broke, get a job instead of gambling on the stock market")
else :
    print(f"Purchasing {qty_to_buy} shares of {stock_symbol}")
    
#BUYING SHARES

buy_order = MarketOrderRequest(
    symbol=stock_symbol,
    qty = qty_to_buy,
    side = OrderSide.BUY,
    time_in_force = TimeInForce.DAY
)

trading_client.submit_order(buy_order)
print(f"Purchased {qty_to_buy} shares of {stock_symbol}")

#HOLDING TIME

days_until_sale = 2
wait_time = (days_until_sale) * 24 * 60 * 60   # dyas * 24 hours * 60 minutes * 60 seconds
hour_time = 60 * 60
test_time = 10 #100 seconds and then sell

for hour in range(24 * days_until_sale):
    print(f"{hour} hour(s) have passed, waiting {(24 * days_until_sale)-hour} hour(s) until selling")
    time.sleep(hour_time)

print(f"{(days_until_sale)} day(s) have PASSED, Selling Shares Now")

# print(f"Waiting {wait_time} seconds before selling...")
# time.sleep(wait_time)



#SELLING SHARES

positions = trading_client.get_all_positions()
stock_position = None
for position in positions:
    if position.symbol == stock_symbol:
        stock_position = position
        break

if stock_position is None:
    print(f"No {stock_symbol} position found. Nothing to sell.")
else:
    qty_to_sell = int(float(stock_position.qty))

    sell_order = MarketOrderRequest(
        symbol=stock_symbol,
        qty=qty_to_sell,
        side=OrderSide.SELL,
        time_in_force=TimeInForce.DAY
    )

    trading_client.submit_order(sell_order)
    print(f"Sold {qty_to_sell} shares of {stock_symbol}")



#DETERMING SUCCESS
#REFRESH ACCOUNT DATA AFTER SELL

update_time = 5 #100 seconds and then sell

print(f"Waiting {update_time} seconds to see results of your Trade")
time.sleep(update_time)

updated_account_data = trading_client.get_account()
new_cash_available = float(updated_account_data.cash)

print(f"New Cash Available: ${new_cash_available}")

if cash_available > new_cash_available :
    print(f"You LOST ${(cash_available - new_cash_available)}")
elif cash_available < new_cash_available : 
    print(f"You MADE ${(new_cash_available - cash_available)}")
else :
    print(f"Broke Even")


#ALTERNATIVE SELL CODE


# trading_client.close_all_positions() #SELL ALL SHARES
# print("All positions closed.")

# new_cash_available = float(account_data.cash)
