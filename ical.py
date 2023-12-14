from icalendar import Calendar, Event
from datetime import datetime, timedelta
from pytz import timezone
import json
from pathlib import Path
import logging


class ICal:
    def __init__(self, teams):
        self.cal = Calendar()
        self.teams = teams

    def _add_header(self, name="kfooty"):
        self.cal.add("prodid", "-//kfooty//")
        self.cal.add("version", "2.0")
        self.cal.add("X-WR-CALNAME", name)

    def _add_event_fixture(self, team="TOT"):
        fixtures = {}

        team_id = self.teams[team]["id"]
        icon = self.teams[team]["icon"]
        fixture_json = f"fixtures/{team_id}.json"

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
        for team in self.teams:
            self._add_event_fixture(team)
        return self.cal.to_ical()

    def create_calendar(self):
        self._add_header()
        for team in self.teams:
            self._add_event_fixture(team)

        with open("calendar.ics", "wb") as f:
            f.write(self.cal.to_ical())
            logging.debug("created calendar.ics")


if __name__ == "__main__":
    with open("team.json") as f:
        teams = json.load(f)
    ical = ICal(teams)
    ical.create_calendar()
