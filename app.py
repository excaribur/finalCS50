from cs50 import SQL
from flask import Flask, render_template

import yfinance as yf

# Configure application
app = Flask(__name__)

@app.route("/")
def index():

    symbol = "PTT"
    stockTH = symbol + ".BK"
    data = yf.Ticker(stockTH).info

    # get stock info
    #data = data.info
 
    return render_template("index.html", data=data, symbol=symbol)

