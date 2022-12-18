import yfinance as yf
import requests

from functools import wraps
from flask import redirect, render_template, session
from cs50 import SQL
from bs4 import BeautifulSoup


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///stock.db")



def getUsers(id):
    # Query database for username
    try:
        users = db.execute("SELECT * FROM users WHERE username = ?", id)
        return users
    except Exception as e:
        print(f"Error : {e}")
        return None


def insertUser(id, hash):
    try:
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", id, hash)
    except Exception as e:
        print(f"Error : {e}")
        return 1
    return 0


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
        prepare = {"symbol": symbol,
                    "name": data["longName"],
                    "price": float(data["currentPrice"]),
                    "sector": data["sector"],
                    "summary": data["longBusinessSummary"]
                    }
        return prepare
    except (KeyError, TypeError, ValueError):
        return {}


def historyStock(symbol):
    #change symbol to uppercase
    symbol = symbol.upper() 
    symbolyf = symbol + ".BK"

    try:
        data = yf.download(symbolyf,period = "1d",ignore_tz = False)
        if data.empty:
            return {}
        price = float(data.iloc[0]["Adj Close"])

        # scrapping name from settrade
        url = f"https://www.settrade.com/th/equities/quote/{symbol}/overview"
        res = requests.get(url)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, 'html.parser') 
        nameTH=soup.find_all("div", class_="col-12 text-secondary fs-24px heading-font-family")
        name = nameTH[0].text
   
        data = {"symbol": symbol,
                "name": name,
                "price": price,
                "sector": "Service in process..",
                "summary": "Service in process.."
                }
        return data
    except (KeyError, TypeError, ValueError):
        return {}


def THB(value):
    """Format value as THB"""
    if  value == 0:
        return ""
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


def getStock(id):
    try:
        rows = db.execute("SELECT * FROM stock WHERE user_id=? ORDER BY symbol", id)
    except Exception as e:
        print(f"Error : {e}")
        return None

    stock = []
    for row in rows:
        info = stockInfo(row["symbol"])
        
        # if not any stock info change to use history from yahoo finance
        if not info:
            info = historyStock(row["symbol"])

        if (not row["resistance"]) or (row["resistance"] < info["price"]) :
            row["resistance"] = 0
        if (not row["support"]) or (row["support"] > info["price"]):
            row["support"] = 0
        prepare =   {"symbol": row["symbol"],
                    "name": info["name"],
                    "sector": info["sector"],
                    "note": row["note"],
                    "resistance": row["resistance"],
                    "price": float(info["price"]),
                    "support": row["support"],
                    "status": row["status"],
                    "summary": info["summary"]
                    }
        stock.append(prepare)
    return stock

def insertStock(symbol, id):
    stock = stockInfo(symbol)
    # if not any stock info change to use history from yahoo finance
    if not stock:
        stock = historyStock(symbol)
    note = "ooooo ooooo ooooo ooooo ooooo ooooo"
    try:
        db.execute("INSERT INTO stock(symbol, note, resistance, support, user_id) VALUES (?,?,?,?,?)",stock["symbol"], note, "", "", id)
    except Exception as e:
        print(f"Error : {e}")
        return 1
    return 0

def delStock(symbol, id):
    stock = stockInfo(symbol)
    # if not any stock info change to use history from yahoo finance
    if not stock:
        stock = historyStock(symbol)
    try:
        db.execute("DELETE FROM stock WHERE symbol=? AND user_id=? ",stock["symbol"], id)
    except Exception as e:
        print(f"Error : {e}")
        return 1
    return 0

def updateStock(symbol, resistance, support, note, id):
    try:
        db.execute("UPDATE stock SET resistance=?, support=?, note=? WHERE symbol=? AND user_id=?", resistance, support, note, symbol, id)
    except Exception as e:
        print(f"Error : {e}")
        return 1
    return 0


def updatePercent(percent, id):
    try:
        db.execute("UPDATE users SET percent=? WHERE id=?", percent, id)
    except Exception as e:
        print(f"Error : {e}")
        return 1
    return 0


def followStock(symbol, status, id):
    try:
        db.execute("UPDATE stock SET status=? WHERE symbol=? AND user_id=?", status, symbol, id)
    except Exception as e:
        print(f"Error : {e}")
        return 1
    return 0

def getFollow(id):
    try:
        rows = db.execute("SELECT * FROM stock WHERE status=? AND user_id=? ORDER BY symbol", "follow", id)
    except Exception as e:
        print(f"Error : {e}")
        return None

    stock = []
    for row in rows:
        info = stockInfo(row["symbol"])
         # if not any stock info change to use history from yahoo finance
        if not info:
            info = historyStock(row["symbol"])

        if (not row["resistance"]) or (row["resistance"] < info["price"]) :
            row["resistance"] = 0
        if (not row["support"]) or (row["support"] > info["price"]):
            row["support"] = 0
        prepare =   {"symbol": row["symbol"],
                    "name": info["name"],
                    "sector": info["sector"],
                    "note": row["note"],
                    "resistance": row["resistance"],
                    "price": float(info["price"]),
                    "support": row["support"],
                    "status": row["status"],
                    "summary": info["summary"]
                    }
        stock.append(prepare)
    return stock

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def checkpwd(password):
    symbol = ["!", "@", "#", "$", "%", "^", "&", "*", "_", "=", "+", "-"]
    al = 0
    num = 0
    sym = 0
    str = ""
    for x in password:
        if x in symbol:
            sym += 1
        if x >= 'a' and x <= 'z' or x >= 'A' and x <= 'Z':
            al += 1
        if x >= '0' and x <= '9':
            num += 1
    if al == 0:
        str += "[a-z] or [A-Z]" + " "
    if num == 0:
        str += "[0-9]" + " "
    if sym == 0:
        str += "!@#$%^&*_=+-"
    if str:
        return f"Password must have at least 1 characters of {str}"
    return "correct"


def getUsername(id):
    try:
        row = db.execute("SELECT username FROM users WHERE id=?", id)
    except Exception as e:
        print(f"Error : {e}")
        return None
    return row[0]["username"]

def getPercent(id):
    try:
        row = db.execute("SELECT percent FROM users WHERE id=?", id)
    except Exception as e:
        print(f"Error : {e}")
        return None
    return row[0]["percent"]

