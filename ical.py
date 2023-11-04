from icalendar import Calendar, Event
from datetime import datetime, timedelta
from pytz import timezone


def get_icalendar():
    cal = Calendar()
    cal.add("prodid", "-//kfooty//")
    cal.add("version", "2.0")

    date = "2023-11-05T15:30:00Z"
    dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    event = Event()
    event.add("summary", "kfooty kick-off")
    event.add("dtstart", dt.date())
    event.add("dtend", dt.date() + timedelta(days=1))
    event.add("dtstamp", datetime.now(timezone("Asia/Seoul")))
    cal.add_component(event)

    return cal
