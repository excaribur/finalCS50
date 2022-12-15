
from flask import Flask, render_template, request, redirect
from service import stockInfo, THB, apology, getStock


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["THB"] = THB



@app.route("/", methods=["GET", "POST"])
def index():

    # retrieve stocks in database and update info
    stock = getStock()

    # User reached route via POST (as by submitting a form via POST)
    quote = None
    if request.method == "POST":
        quote = request.form.get("quote")
        quote = stockInfo(quote)

    message = "Not found"
    if (quote):
        message = quote["name"] + "(" + quote["symbol"] + ")" + "   " + THB(quote["price"])
    if not (quote):
        for row in stock:
            if quote["symbol"] == row["symbol"]:
                message = "You got it already: " + quote["name"] + "(" + quote["symbol"] + ")" + "   " + THB(quote["price"])
                break
    return render_template("index.html", stock=stock ,message=message)


@app.route("/info")
def info():
    return render_template("info.html")

@app.route("/monitor")
def watch():
    return render_template("watch.html")