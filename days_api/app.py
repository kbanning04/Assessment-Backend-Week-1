"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime, date

from flask import Flask, Response, request, jsonify

from date_functions import (convert_to_datetime, get_day_of_week_on,
                            get_days_between, get_current_age, convert_weird_format)

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
        except ValueError:
            return {"error": "Unable to convert value to datetime."}, 400

        days_between = get_days_between(first_date, last_date)
        return {"days": days_between}
    return {"error": "Method not defined"}, 405


@app.route("/weekday", methods=["POST"])
def get_weekday():
    """ Returns which day of a week a date is. """
    if request.method == "POST":
        weekday_date_response = request.json
        if "date" not in weekday_date_response:
            return {"error": "Missing required data."}, 400
        try:
            weekday_date = convert_to_datetime(weekday_date_response["date"])
        except ValueError:
            return {"error": "Unable to convert value to datetime."}, 400
        weekday = get_day_of_week_on(weekday_date)
        return {"weekday": weekday}
    return {"error": "Method not defined"}, 405


@app.route("/history", methods=["GET", "DELETE"])
def get_history():
    """ Returns the last n requests made. """
    if request.method == "GET":
        number = request.args.get("number")
        if number is None:
            number = 5
        try:
            number = int(number)
        except ValueError:
            return {"error": "Number must be an integer between 1 and 20."}, 400
        if number > 20 or number < 1:
            return {"error": "Number must be an integer between 1 and 20."}, 400
        i = number
        history_length = len(app_history)
        returned_list = []
        while i <= history_length:
            returned_list.append(app_history[i])
            i += 1
        return returned_list
    if request.method == "DELETE":
        clear_history()
        return {"status": "History cleared"}
    return {"error": "Method not defined"}, 405


@app.route("/current_age", methods=["GET"])
def gets_current_age():
    """ Returns the current age when given a birthdate. """
    if request.method == "GET":
        wrong_format_date = request.args.get("date")
        if wrong_format_date is None:
            return {"error": "Date parameter is required."}, 400
        try:
            birth_date = convert_weird_format(wrong_format_date)
        except ValueError:
            return {"error": "Value for date parameter is invalid."}, 400
        age = get_current_age(birth_date)
        return {"current_age": age}
    return {"error": "Method not defined"}, 405


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(port=8080, debug=True)
