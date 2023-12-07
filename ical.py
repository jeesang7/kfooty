from icalendar import Calendar, Event
from datetime import datetime, timedelta
from pytz import timezone
import json
from pathlib import Path
import logging


TOT = "fixtures/47.json"
PSG = "fixtures/85.json"
BAY = "fixtures/157.json"


class ICal:
    def __init__(self):
        self.cal = Calendar()

    def _add_header(self, name="kfooty"):
        self.cal.add("prodid", "-//kfooty//")
        self.cal.add("version", "2.0")
        self.cal.add("X-WR-CALNAME", name)

    def _add_event_fixture(self, fixture_json=TOT):
        fixtures = {}

        icon = ""
        if fixture_json == TOT:
            icon = "⚽️🏴󠁧󠁢󠁥󠁮󠁧󠁿"
        elif fixture_json == PSG:
            icon = "⚽️🇫🇷"
        elif fixture_json == BAY:
            icon = "⚽️🇩🇪"

        with open(fixture_json) as f:
            fixtures = json.load(f)

        for fixture in fixtures["response"]:
            date = fixture["fixture"]["date"]
            home = fixture["teams"]["home"]["name"]
            away = fixture["teams"]["away"]["name"]
            # print(date, home, away)

            event = Event()
            dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
            event.add("summary", icon + home + " v " + away)
            event.add("dtstart", dt)
            event.add("dtend", dt + timedelta(hours=2))
            event.add("dtstamp", datetime.now(timezone("Asia/Seoul")))
            self.cal.add_component(event)

    def get_calendar(self, ics="calendar.ics"):
        if Path(ics).exists():
            with open(ics, "r") as f:
                cal = f.read()
            return cal

        self._add_header()
        self._add_event_fixture()
        self._add_event_fixture(PSG)
        self._add_event_fixture(BAY)
        return self.cal.to_ical()

    def create_calendar(self):
        self._add_header()
        self._add_event_fixture()
        self._add_event_fixture(PSG)
        self._add_event_fixture(BAY)

        with open("calendar.ics", "wb") as f:
            f.write(self.cal.to_ical())
            logging.debug("created calendar.ics")


if __name__ == "__main__":
    ical = ICal()
    ical.create_calendar()
