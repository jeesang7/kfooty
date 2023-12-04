from flask import Flask, make_response
from ical import ICal
from scheduler import Scheduler

app = Flask(__name__)


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
