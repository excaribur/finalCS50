import yfinance as yf

from cs50 import SQL
from flask import render_template

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///stock.db")

def stockInfo(symbol):
    """ 
    get stock info from yahoofinace by
    https://pypi.org/project/yfinance/
    """
    #change symbol to uppercase
    symbol = symbol.upper() 
    symbolyf = symbol + ".BK"
    try:
        data = yf.Ticker(symbolyf).info
        return {"symbol": symbol,
        "name": data["longName"],
        "price": float(data["currentPrice"]),
        "sector": data["sector"],
        "summary": data["longBusinessSummary"]
        }
    except (KeyError, TypeError, ValueError):
        return {}

def THB(value):
    """Format value as THB"""
    return f"฿{value:,.2f}"

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def getStock():
    try:
        rows = db.execute("SELECT * FROM stock")
    except Exception as e:
        print(f"Error : {e}")
        return None

    stock = []
    
    for row in rows:
        info = stockInfo(row["symbol"])
        #set NUll == ""
        if not row["resistance"]:
            row["resistance"] = ""
        if not row["support"]:
            row["support"] = ""
        prepare =   {"symbol": row["symbol"],
                    "name": info["name"],
                    "sector": info["sector"],
                    "note": row["note"],
                    "resistance": row["resistance"],
                    "price": info["price"],
                    "support": row["support"],
                    "status": row["status"],
                    }
        stock.append(prepare)
    return stock
