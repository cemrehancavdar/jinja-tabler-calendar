from datetime import datetime, timedelta

from flask import Flask, render_template
import itertools
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())


def generate_calendar(date_input: str | datetime) -> list[datetime]:
    # Check if date_input is a string
    if isinstance(date_input, str):
        # Convert string to datetime object
        current_date = datetime.strptime(date_input, "%Y-%m-%d")
    elif isinstance(date_input, datetime):
        # If it's already a datetime object, use it directly
        current_date = date_input
    else:
        raise TypeError(
            "date_input must be a string in the format 'YYYY-MM-DD' or a datetime object"
        )

    year = current_date.year
    month = current_date.month

    # Find the first day of the month
    first_day_of_month = datetime(year, month, 1)

    # Find the day of the week for the first day of the month (0 = Monday, 6 = Sunday)
    first_day_of_week = first_day_of_month.weekday()

    # Calculate how many days to go back to reach Monday if the first day is not Monday
    days_to_subtract = (first_day_of_week) % 7

    # Calculate the start date of the calendar by subtracting days_to_subtract from the current date
    start_date = first_day_of_month - timedelta(days=days_to_subtract)

    # Create a list to hold the calendar dates
    calendar_dates = []

    # Loop through 42 days (6 weeks)
    for _ in range(42):
        calendar_dates.append(start_date)
        start_date += timedelta(days=1)

    return calendar_dates


def is_in_year_and_month(date: datetime, year: int, month: int) -> bool:
    return date.year == year and date.month == month



app = Flask(__name__)


class Event:
    def __init__(self, date: datetime, title: str, description: str):
        self.date = date
        self.title = title
        self.description = description


@app.route("/")
def home():
    year = 2024
    month = 1
    day = 2

    calendar = generate_calendar("2024-02-02")
    chunks = list(itertools.batched(calendar, 7))

    events = [
        Event(datetime(2024, 2, 1), "Item 1", "This is an item"),
        Event(datetime(2024, 2, 1), "Item 2", "This is an item"),
        Event(datetime(2024, 2, 1), "Item 3", "This is an item"),
        Event(datetime(2024, 2, 1), "Item 4", "This is an item"),
        Event(datetime(2024, 2, 1), "Item 5", "This is an item"),
        Event(datetime(2024, 2, 1), "Item 6", "This is an item"),
        Event(datetime(2024, 2, 1), "Item 7", "This is an item"),
        Event(datetime(2024, 2, 1), "Item 8", "This is an item"),
        Event(datetime(2024, 2, 1), "Item 9", "This is an item"),
        Event(datetime(2024, 2, 3), "Item 10", "This is an item"),
        Event(datetime(2024, 2, 5), "Item 11", "This is an item"),
    ]

    grouped_events = {
        k: list(v) for k, v in itertools.groupby(events, key=lambda x: x.date)
    }
    print(grouped_events)
    return render_template(
        "calendar.html",
        chunks=chunks,
        calendar=calendar,
        grouped_events=grouped_events,
        is_in_year_and_month=is_in_year_and_month,
        year=year,
        month=month,
        _day=day,
    )


if __name__ == "__main__":
    app.run(debug=True)
