from icalendar import Calendar, Event
from datetime import datetime, timedelta
from pytz import timezone
import json


def get_icalendar():
    cal = Calendar()
    cal.add("prodid", "-//kfooty//")
    cal.add("version", "2.0")
    cal.add("X-WR-CALNAME", "kfooty")

    date = "2023-11-05T15:30:00Z"
    dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    event = Event()
    event.add("summary", "kfooty kick-off")
    event.add("dtstart", dt.date())
    event.add("dtend", dt.date() + timedelta(days=1))
    event.add("dtstamp", datetime.now(timezone("Asia/Seoul")))
    cal.add_component(event)

    return cal


def get_tot(fixture_json="fixtures_tot.json"):
    cal = Calendar()
    cal.add("prodid", "-//kfooty//")
    cal.add("version", "2.0")
    cal.add("X-WR-CALNAME", "kfooty")

    fixtures_tot = {}
    with open(fixture_json) as f:
        fixtures_tot = json.load(f)

    for fixture in fixtures_tot["response"]:
        date = fixture["fixture"]["date"]
        home = fixture["teams"]["home"]["name"]
        away = fixture["teams"]["away"]["name"]
        # print(date, home, away)

        event = Event()
        dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        event.add("summary", "⚽️ 🏴󠁧󠁢󠁥󠁮󠁧󠁿 " + home + " v " + away)
        event.add("dtstart", dt)
        event.add("dtend", dt + timedelta(hours=2))
        event.add("dtstamp", datetime.now(timezone("Asia/Seoul")))
        cal.add_component(event)

    return cal


if __name__ == "__main__":
    get_tot()
