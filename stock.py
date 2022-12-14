import yfinance as yf

# get stock info
def stockInfo(symbol):
    #change symbol to uppercase
    symbol = symbol.upper()
    
    data = yf.Ticker(symbol).info
    return {"symbol": symbol,
            "name": data["longName"],
            "price": data["currentPrice"],
            "sector": data["sector"],
            "Summary": data["longBusinessSummary"]
            }