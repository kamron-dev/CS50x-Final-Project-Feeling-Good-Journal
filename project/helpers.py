import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


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


def get_result(total_count):
    step = 1
    if total_count in range(0, 5 + step, step):
        return "No depression, Feeling good!"
    elif total_count in range(6, 10 + step, step):
        return "Normal but unhappy, feeling a bit on the lumpy side!"
    elif total_count in range(11, 25 + step, step):
        return "Mild depression, should not be a cause of alarm, but consider treatment if score remains in this range for several weeks!"
    elif total_count in range(26, 50 + step, step):
        return "Moderate Depression, consider treatment if score remains in this range  for more than two weeks!"
    elif total_count in range(51, 75 + step, step):
        return "Severe depression, consider seeking treatment!"
    elif total_count in range(76, 100 + step, step):
        return "Extreme depression, intesely uncomfortable, seek professional help!"




