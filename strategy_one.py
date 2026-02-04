import time
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import OrderStatus

#API KEY and API SECRET change depending on which account to use


api_KEY = "PKZCWBE2G4KCQ37BU4JF2FZLIN"
api_SECRET = "GzYKMF3GmnkQbnk7Rpi2xSuRWQDXynMnEifv4Ns891E"
stock_symbol = "KTOS"

trading_client = TradingClient(api_KEY , api_SECRET, paper=True) 
data_client = StockHistoricalDataClient(api_KEY, api_SECRET)

#ACCOUNT DATA

account_data = trading_client.get_account()
cash_available = float(account_data.cash)
print(f"Cash Available: ${cash_available}")

#COLLECTING LMT STOCK PRICE and determing amount of LMT shares to BUY

quote_request = StockLatestQuoteRequest(symbol_or_symbols=stock_symbol)
quote = data_client.get_stock_latest_quote(quote_request)[stock_symbol]
price = float(quote.ask_price or quote.bid_price)  
print(f"{stock_symbol} price: ${price:.2f}")


qty_to_buy = int(cash_available // (price))
if qty_to_buy <= 0:
    raise Exception("You are broke, get a job instead of gambling on defense shares")
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

#SELLING SHARES

wait_time = 1 * 24 * 60 * 60   #Change the '1' to changed the number of days
test_time = 10 #100 seconds and then sell

print(f"Waiting {wait_time} seconds before selling...")
time.sleep(wait_time)

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
# REFRESH ACCOUNT DATA AFTER SELL

update_time = 5 #100 seconds and then sell

print(f"Waiting {update_time} seconds to see results of your Trade")
time.sleep(update_time)

updated_account_data = trading_client.get_account()
new_cash_available = float(updated_account_data.cash)

# trading_client.close_all_positions() #SELL ALL SHARES
# print("All positions closed.")

# new_cash_available = float(account_data.cash)
print(f"New Cash Available: ${new_cash_available}")

if cash_available > new_cash_available :
    print(f"You LOST ${(cash_available - new_cash_available)}")
elif cash_available < new_cash_available : 
    print(f"You MADE ${(new_cash_available - cash_available)}")
else :
    print(f"Broke Even")
# #trading_client.close_all_positions()
