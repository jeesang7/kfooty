from icalendar import Calendar, Event
from datetime import datetime, timedelta
from pytz import timezone
import json
from pathlib import Path
import logging
import zipfile
import requests
import os


class ICal:
    def __init__(self, teams, ics_path="static/calendar.ics"):
        self.cal = Calendar()
        self.teams = teams
        self.ics_path = ics_path

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

    def get_calendar(self):
        ics = self.ics_path
        if Path(self.ics).exists():
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

        with open(self.ics_path, "wb") as f:
            f.write(self.cal.to_ical())
            logging.debug(f"created {self.ics_path}")

    def deploy_calendar(self, zip="calendar.zip"):
        with zipfile.ZipFile(zip, "w") as z:
            for f in os.listdir("static"):
                z.write("static/" + f, f)

        site_id = os.environ.get("NETLIFY_SITE_ID", "")
        url = f"https://api.netlify.com/api/v1/sites/{site_id}/deploys"

        token = os.environ.get("NETLIFY_ACCESS_TOKEN", "")
        headers = {
            "Content-Type": "application/zip",
            "Authorization": f"Bearer {token}",
        }

        with open(zip, "rb") as f:
            response = requests.post(url, headers=headers, data=f)

        if response.status_code != 200:
            logging.error(f"deploy not 200 {response.reason}")
        logging.debug(f"deploy completed. {response.content}")


if __name__ == "__main__":
    with open("team.json") as f:
        teams = json.load(f)
    ical = ICal(teams)
    ical.create_calendar()
    ical.deploy_calendar()
