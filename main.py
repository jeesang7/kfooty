from flask import Flask, make_response
import ical

app = Flask(__name__)


@app.route("/ical")
def get_ical():
    response = make_response(ical.get_tot().to_ical())
    response.headers["Content-Disposition"] = "attachment; filename=calendar.ics"
    return response


if __name__ == "__main__":
    app.run(debug=True)
