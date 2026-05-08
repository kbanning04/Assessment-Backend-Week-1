"""Functions for working with dates."""

from datetime import datetime, date


def convert_to_datetime(date_val: str) -> datetime:
    """ Converts a date in the form of a string to a datetime. """
    try:
        datetime_format = datetime.strptime(f"{date_val}", "%d.%m.%Y")
    except ValueError as e:
        raise ValueError("Unable to convert value to datetime.")
    return datetime_format


def get_days_between(first: datetime, last: datetime) -> int:
    """ Returns the number of days between two dates. """
    if not isinstance(first, datetime) or not isinstance(last, datetime):
        raise TypeError("Datetimes required.")
    delta = (last - first).days
    return delta


def get_day_of_week_on(date_val: datetime) -> str:
    """ Returns which day of the week a date is. """
    if not isinstance(date_val, datetime):
        raise TypeError("Datetime required.")
    weekday_converted = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }
    weekday = date_val.weekday()

    return weekday_converted[weekday]


def get_current_age(birthdate: date) -> int:
    """ Returns the current age when given a birthdate. """
    if not isinstance(birthdate, date):
        raise TypeError("Date required.")
    current_day = date.today()
    delta = (current_day - birthdate).days // 365.25
    return round(delta)
