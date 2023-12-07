from apscheduler.schedulers.background import BackgroundScheduler
import requests
from datetime import datetime, timedelta
import os
import json
import logging
from ical import ICal

TOT = "47"
PSG = "85"
BAY = "157"


class Scheduler:
    def fetch_fixtures(self, team_id=TOT):
        self.fetched_fixtures = {}
        today = datetime.now().date()
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

        querystring = {
            "season": "2023",
            "team": team_id,
            "from": str(today),
            "to": str(today + timedelta(weeks=2)),
            "timezone": "Asia/Seoul",
        }

        headers = {
            "X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""),
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com",
        }

        response = requests.get(url, headers=headers, params=querystring)
        self.fetched_fixtures = response.json()
        # logging.debug("fetched_fixtures response.json: " + str(self.fetched_fixtures))

        """
        fname = f"fetch_fixtures_{team_id}_{today}.json"
        with open(fname, "w") as f:
            json.dump(response.json(), f)
        """

    def update_fixtures(self, team_id=TOT):
        logging.debug(f"update_fixtrue start: {team_id}")
        fixture_json = "fixtures/" + team_id + ".json"
        with open(fixture_json) as f:
            fixtures = json.load(f)

        on_write = False
        for fetched_fixture in self.fetched_fixtures["response"]:
            # logging.debug("fetched_fixture: " + str(fetched_fixture))

            _id = fetched_fixture["fixture"]["id"]
            ts = fetched_fixture["fixture"]["timestamp"]
            date = fetched_fixture["fixture"]["date"]
            date = date.replace("+09:00", "Z")
            for i, fixture in enumerate(fixtures["response"]):
                if (
                    fixture["fixture"]["id"] == _id
                    and fixture["fixture"]["timestamp"] != ts
                ):
                    fixtures["response"][i]["fixture"]["timestamp"] = ts
                    fixtures["response"][i]["fixture"]["date"] = date
                    logging.debug(f"{team_id} - fixture updated: {i} {_id} {ts} {date}")
                    on_write = True

        if on_write:
            with open(fixture_json, "w") as f:
                json.dump(fixtures, f)
            logging.debug(f"overwritten done: {fixture_json}")
        else:
            logging.debug("no update")

    def check_fixtures(self):
        self.fetch_fixtures()
        self.update_fixtures()
        self.fetch_fixtures(PSG)
        self.update_fixtures(PSG)
        self.fetch_fixtures(BAY)
        self.update_fixtures(BAY)
        ical = ICal()
        ical.create_calendar()

    def start(self):
        scheduler = BackgroundScheduler(timezone="Asia/Seoul")
        scheduler.add_job(self.check_fixtures, "cron", hour=23, minute=36)
        scheduler.start()
        logging.debug("start BackgroundScheduler every 23:36")


if __name__ == "__main__":
    sched = Scheduler()
    sched.start()

    import time

    while True:
        time.sleep(2)
