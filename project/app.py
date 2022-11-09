import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
from helpers import get_result

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

# Make sure API key is set



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "GET":

        return render_template("index.html")




@app.route("/journal", methods=["GET", "POST"])
@login_required
def journal():
    # Defining the user_id
    user_id = session["user_id"]
    if (request.method == 'POST'):
        no = request.form.get("delete")
        db.execute("DELETE FROM journal WHERE test_id = ?", no)
        return render_template("delete_success.html")
    else:
        """Show mood journal entries"""
        # Running an sql query to obtain data to the journal variable
        journal = db.execute("SELECT * FROM journal WHERE user_id = ?", user_id)

        # Rendering the journal template
        return render_template("journal.html", journal = journal)


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

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/test", methods=["GET", "POST"])
@login_required
def test():
    """Taking test"""
    # Defining userid
    user_id = session["user_id"]
    if request.method == "POST":
        i = 0
        total_count = 0
    # Iterating through test questions with a while loop
        while True:
            button_name = 'inlineRadioOptions' + str(i)
            if request.form.get(button_name) is not None:
                total_count += int(request.form.get(button_name))
                i += 1
    # Getting the result with get_result function defined in helpers.py
                result = get_result(total_count)
            else:
                break
    # Inserting the test result in the journal database
        db.execute("INSERT INTO journal (user_id, score) VALUES (?, ?)", user_id, total_count)

    # Rendering the success template with total score of the test and the interpretation of the score
        return render_template("success.html", total_count=total_count, result=result)


    else:
        return render_template("test.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if (request.method == "POST"):
        # Getting the values of username and password from the forms
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        # Handling the errors
        if not username:
            return apology('Username is required!')
        elif not password:
            return apology('Password is required!')
        elif not confirmation:
            return apology('Password confirmation is required!')

        if confirmation != password:
            return apology('Passwords should match!')

        # Generating the hash
        hash = generate_password_hash(password)
        # Registering the user in the database
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
            return redirect('/')
        except:
            return apology('Username already exists!')

    else:
        return render_template("register.html")





