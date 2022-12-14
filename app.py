from cs50 import SQL
from flask import Flask, render_template
from stock import stockInfo

import yfinance as yf

# Configure application
app = Flask(__name__)

@app.route("/")
def index():

    # get stock info
    symbol = "PTT" + ".BK"
    stock = stockInfo(symbol)

    return render_template("index.html", stock=stock)

