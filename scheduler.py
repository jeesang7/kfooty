from apscheduler.schedulers.background import BackgroundScheduler
import requests
from datetime import datetime, timedelta
import os
import json
import logging
from ical import ICal


class Scheduler:
    def __init__(self, teams):
        self.teams = teams

    def fetch_fixtures(self, team="TOT"):
        team_id = self.teams[team]["id"]

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

    def update_fixtures(self, team="TOT"):
        team_id = self.teams[team]["id"]
        logging.debug(f"update_fixtrue start: {team_id}")
        fixture_json = f"fixtures/{team_id}.json"
        with open(fixture_json) as f:
            fixtures = json.load(f)

        fixture_ids = []
        for fixture in fixtures["response"]:
            fixture_ids.append(fixture["fixture"]["id"])

        on_write = False
        fetched_fixture_ids = []
        new_fixtures = []
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

            # find new fixture
            fetched_fixture_ids.append(_id)

            if _id not in fixture_ids:
                fetched_fixture["fixture"]["date"] = date
                logging.debug(f"{team_id} - fixture new: {_id} {date}")
                new_fixtures.append(fetched_fixture)
                on_write = True

        if on_write:
            for new_fixture in new_fixtures:
                fixtures["response"].append(new_fixture)
            with open(fixture_json, "w") as f:
                json.dump(fixtures, f)
            logging.debug(f"overwritten done: {fixture_json}")
        else:
            logging.debug("no update")

    def check_fixtures(self):
        for team in self.teams:
            self.fetch_fixtures(team)
            self.update_fixtures(team)

        ical = ICal(self.teams)
        ical.create_calendar()
        ical.deploy_calendar()

    def start(self):
        h = os.environ.get("CRON_HOUR", "17")
        m = os.environ.get("CRON_MINUTE", "10")

        scheduler = BackgroundScheduler(timezone="Asia/Seoul")
        scheduler.add_job(
            self.check_fixtures,
            "cron",
            hour=h,
            minute=m,
        )
        scheduler.start()
        logging.debug(f"start BackgroundScheduler every {h}:{m}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    with open("team.json") as f:
        teams = json.load(f)
    sched = Scheduler(teams)
    sched.start()

    import time

    while True:
        time.sleep(2)
