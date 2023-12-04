from flask import Flask, make_response
from ical import ICal
from scheduler import Scheduler
import logging

logging.basicConfig(level=logging.DEBUG)


def create_app():
    ical = ICal()
    ical.create_calendar()

    scheduler = Scheduler()
    scheduler.start()

    app = Flask(__name__)

    return app


app = create_app()


@app.route("/ical")
def get_ical():
    response = make_response(ICal().get_calendar())
    response.headers["Content-Disposition"] = "attachment; filename=calendar.ics"
    return response


if __name__ == "__main__":
    ical = ICal()
    ical.create_calendar()

    scheduler = Scheduler()
    scheduler.start()

    app.run(debug=True)
