"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime, date

from flask import Flask, Response, request, jsonify

from date_functions import (convert_to_datetime, get_day_of_week_on,
                            get_days_between, get_current_age)

app_history = []

app = Flask(__name__)


def add_to_history(current_request):
    """Adds a route to the app history."""
    app_history.append({
        "method": current_request.method,
        "at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "route": current_request.endpoint
    })


def clear_history():
    """Clears the app history."""
    app_history.clear()


@app.get("/")
def index():
    """Returns an API welcome message."""
    return jsonify({"message": "Welcome to the Days API."})


@app.route("/between", methods=["POST"])
def get_days_between_two() -> date:
    """ Gets the number of days between two dates. """
    if request.method == "POST":
        dates = request.json
        if "first" not in dates or "last" not in dates:
            return {"error": "Missing required data."}, 400
        first = dates["first"]
        last = dates["last"]
        try:
            first_date = convert_to_datetime(first)
            last_date = convert_to_datetime(last)
        except ValueError as e:
            return {"error": "Unable to convert value to datetime."}, 400

        days_between = get_days_between(first_date, last_date)
        return {"days": days_between}
    return {"error": "Method not defined"}, 405


@app.route("/weekday", methods=["POST"])
def get_weekday():
    if request.method == "POST":
        weekday_date_response = request.json
        if "date" not in weekday_date_response:
            return {"error": "Missing required data."}, 400
        try:
            weekday_date = convert_to_datetime(weekday_date_response["date"])
        except ValueError as e:
            return {"error": "Unable to convert value to datetime."}, 400
        weekday = get_day_of_week_on(weekday_date)
        return {"weekday": weekday}
    return {"error": "Method not defined"}, 405


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(port=8080, debug=True)
