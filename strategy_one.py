import sys

print(sys.executable)

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

api_KEY = "PKYJMWD7EIHKV3EZM5I66PLBUH"
api_SECRET = "pkiuWYM2x2kBNzijWXTDVNwSciYmgvpeukP1YTrrcJp"
stock_symbol = "TWI"

trading_client = TradingClient(api_KEY , api_SECRET, paper=True) 
data_client = StockHistoricalDataClient(api_KEY, api_SECRET)

#ACCOUNT DATA

account_data = trading_client.get_account()
cash_available = float(account_data.cash)
print(f"Cash Available: ${cash_available}")

#Checking is Market is OPEN Method

def market_open():
        clock = trading_client.get_clock()
        while not clock.is_open:
            next_open = clock.next_open
            now = clock.timestamp

            if next_open.tzinfo:
                now = now.replace(tzinfo=next_open.tzinfo)
            
            seconds_until_open = (next_open - now).total_seconds()
            hours_until_open = seconds_until_open / 3600
            print(f"Market is CLOSED")
            print(f"Will open at: {next_open}")
            print(f"That's in {hours_until_open:.1f} hours ({int(seconds_until_open)} seconds)")
            print(f"Sleeping until market opens + 20 seconds...")
            time.sleep(max(seconds_until_open + 20, 0))

            clock = trading_client.get_clock()
          # SINGLE SLEEP until Market Opens
            
        
        print("✅ Market should be open now!")
        print("Market is OPEN")

#COLLECTING STOCK PRICE and determing amount of shares to BUY

market_open() #Determining if the Market is OPEN

quote_request = StockLatestQuoteRequest(symbol_or_symbols=stock_symbol)
quote = data_client.get_stock_latest_quote(quote_request)[stock_symbol]
price = float(quote.ask_price or quote.bid_price)  
print(f"{stock_symbol} price: ${price:.2f}")


qty_to_buy = int(cash_available // (price))
if qty_to_buy <= 0:
    raise Exception("You are broke, get a job instead of gambling on the stock market")
else :
    print(f"Attempting to purchase {qty_to_buy} shares of {stock_symbol}")
    
#BUYING SHARES

buy_order = MarketOrderRequest(
    symbol=stock_symbol,
    qty = qty_to_buy,
    side = OrderSide.BUY,
    time_in_force = TimeInForce.DAY
)


trading_client.submit_order(buy_order)
print(f"Successfully Purchased {qty_to_buy} shares of {stock_symbol}")

#HOLDING TIME

days_until_sale = 2
wait_time = (days_until_sale) * 24 * 60 * 60   # days * 24 hours * 60 minutes * 60 seconds


print(f"Waiting {days_until_sale} days before selling...")
time.sleep(wait_time)


#SELLING SHARES
market_open()


print(f"Selling all available {stock_symbol} positions")

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

update_time = 15 #100 seconds and then sell

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


#ALTERNATIVE SELL CODE, SELL ALL POSITIONS


# trading_client.close_all_positions() #SELL ALL SHARES
# print("All positions closed.")

# new_cash_available = float(account_data.cash)


    
