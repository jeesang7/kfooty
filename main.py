from flask import Flask, make_response
from ical import ICal
from scheduler import Scheduler
import logging
import json

logging.basicConfig(level=logging.DEBUG)


def create_app():
    with open("team.json") as f:
        teams = json.load(f)
    ical = ICal(teams)
    ical.create_calendar()

    scheduler = Scheduler(teams)
    scheduler.check_fixtures()
    scheduler.start()

    app = Flask(__name__)

    return app


app = create_app()


@app.route("/ical")
def get_ical():
    with open("team.json") as f:
        teams = json.load(f)
    ical = ICal(teams)
    response = make_response(ical.get_calendar())
    response.headers["Content-Disposition"] = "attachment; filename=calendar.ics"
    return response


if __name__ == "__main__":
    with open("team.json") as f:
        teams = json.load(f)
    ical = ICal(teams)
    ical.create_calendar()

    scheduler = Scheduler(teams)
    scheduler.start()

    app.run(debug=True)
