import yfinance as yf

def stockInfo(symbol):
 # get stock info
    data = yf.Ticker(symbol).info

    return {"symbol": symbol,
            "name": data["longName"],
            "price": data["currentPrice"],
            "sector": data["sector"],
            "Summary": data["longBusinessSummary"],
            }