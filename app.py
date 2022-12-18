
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from service import stockInfo, THB, apology, getStock, insertStock, delStock
from service import updateStock, followStock, getFollow, getUsers, historyStock
from service import login_required, checkpwd, insertUser, getUsername, getPercent, updatePercent


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["THB"] = THB
app.jinja_env.filters["getUsername"] = getUsername
app.jinja_env.filters["getPercent"] = getPercent

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    # Fetch id from session
    id = session["user_id"]
    # retrieve stocks in database and update info
    stock = getStock(id)

    # User reached route via POST (as by submitting a form via POST)
    quote = None
    if request.method == "POST":
        getquote = request.form.get("quote")
        if not getquote:
            return apology("please fill in symbol")
        quote = stockInfo(getquote)
        # if not any stock info change to use history from yahoo finance
        if not quote:
            quote = historyStock(getquote)

    message = ""
    if (quote):
        for row in stock:
            if quote["symbol"] == row["symbol"]:
                message = 1
                return render_template("index.html", stock=stock ,message=message)
        message = quote
    
    return render_template("index.html", stock=stock ,message=message)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        id = request.form.get("username")
        # Query database for username
        rows = getUsers(id)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide username")

        # Ensure and confirm password
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("must provide matched re-password ")

        # check pwd pattern Require users’ passwords to have some number of letters, numbers, and/or symbols.
        message = checkpwd(request.form.get("password"))
        if message != "correct":
            return apology(message)

        # create hash password
        hash = generate_password_hash(request.form.get("password"), method="pbkdf2:sha256",
                                      salt_length=len(request.form.get("password")))

        id = request.form.get("username") 
        # Insert database for username
        if(insertUser(id, hash)):
            return apology("Username is not avaliable")
         
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    # Fetch id from session
    id = session["user_id"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol")

    # insert stock
    if(insertStock(symbol, id)):
        return apology("cannot insert data")

    return redirect("/")


@app.route("/info" , methods=["GET", "POST"])
@login_required
def info():

    # Fetch id from session
    id = session["user_id"]    

    # User reached route via GET (as by clicking a link or via redirect)
    symbol = request.args.get('symbol')

    # retrieve stocks in database and update info
    stock = getStock(id)
    for row in stock:

        if row["symbol"] == symbol:
            return render_template("info.html", stock=row)

    return redirect("/")


@app.route("/follow", methods=["GET", "POST"])
@login_required
def follow():

    # Fetch id from session
    id = session["user_id"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("follow")
        support = "follow"
        # update status in stock table  to follow
        if(followStock(symbol, support, id)):
            return apology("cannot follow")

    # retrieve stocks in database and update info
    stock = getFollow(id)

    return render_template("follow.html", stock=stock)
   

@app.route("/unfollow", methods=["GET", "POST"])
@login_required
def unfollow():
    # Fetch id from session
    id = session["user_id"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("unfollow")
        status = "unfollow"
        # update status in stock table  to follow
        if(followStock(symbol, status, id)):
            return apology("cannot request")

    return redirect("/follow")
   

@app.route("/save", methods=["GET", "POST"])
@login_required
def save():

     # Fetch id from session
    id = session["user_id"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        #symbol = request.query_string
        symbol = request.args.get('symbol')
        resistance = request.form.get("resistance")
        support = request.form.get("support")
        note = request.form.get("note")

    # update stock
    if(updateStock(symbol, resistance, support, note, id)):
         return apology("cannot insert data")

    return redirect("/")


@app.route("/cal", methods=["GET", "POST"])
@login_required
def cal():
    # Fetch id from session
    id = session["user_id"]

    # retrieve stocks in database and update info
    stock = getFollow(id)

    # User reached route via POST (as by submitting a form via POST)
    shares=[]
    total = 0
    if request.method == "POST":
        for row in stock:
            info = historyStock(row["symbol"])
            shsymbol = "sh" + row["symbol"]
            share = int(request.form.get(shsymbol))
            value = info["price"] * share
            prepare={"symbol": row["symbol"],
                     "share": share,
                     "total": value
            }
            total += value
            shares.append(prepare)
    return render_template("follow.html", shares=shares, stock=stock, total=total)


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    # Fetch id from session
    id = session["user_id"]

     # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("delete")
    # insert stock
    if (delStock(symbol, id)):
        return apology("cannot delete data")
    return redirect("/")


@app.route("/scan", methods=["GET", "POST"])
@login_required
def scan():
    # Fetch id from session
    id = session["user_id"]

     # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        percent = float(request.form.get("percent"))
        
    # retrieve stocks in database and update info
    stock = getStock(id)
    if percent <= 0 or percent > 100:
        return redirect("/")
    # Collect stock only resistance and support are in percent range

    # Update percent in database
    if(updatePercent(percent, id)):
        return apology('cannot update percent')
    
    collect=[]
    for row in stock:
        price = row["price"]
        resist = row["resistance"]
        support = row["support"]
        upper = 1 + percent / 100
        lower = 1 - percent / 100
        save = 0
        if  price >= lower * resist and price <= resist: 
            collect.append(row)
            save = 1
        if price <= upper * support and price >= resist and save == 0:
            collect.append(row)

    return render_template("index.html", stock=collect)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)




