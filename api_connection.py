""" This module holds APIConnection, which is a class that can pull data from the AoE 4 API """

import math

import requests
import pandas as pd

# Regions for request:
# Europe = 0
# MiddleEast = 1
# Asia = 2
# NorthAmerica = 3
# SouthAmerica = 4
# Oceania = 5
# Africa = 6
# Global = 7


class APIConnection:
    """Makes the connection to the AoE 4 API"""

    def __init__(self) -> None:

        self.api_url = "https://api.ageofempires.com/api/ageiv/Leaderboard"
        self.headers = {
            "content-type": "application/json",
            "Accept": "application/json",
        }

    def _make_post_request(self, payload):
        r = requests.post(self.api_url, json=payload, headers=self.headers)
        return r.json()

    def get_all_data(self) -> pd.DataFrame:
        count_per_page = 100
        initial_payload = {
            "region": 7,
            "versus": "players",
            "matchType": "unranked",
            "teamSize": "1v1",
            "searchPlayer": "",
            "page": "1",
            "count": str(count_per_page),
        }

        first_request = self._make_post_request(initial_payload)
        total_players = first_request["count"]
        total_pages = math.ceil(total_players / count_per_page)

        df_results = pd.DataFrame(data=first_request["items"])

        for page_num in range(1, total_pages + 1):
            payload = initial_payload.copy()
            payload["page"] = str(page_num)
            data_json = self._make_post_request(payload)
            df_page = pd.DataFrame(data=data_json["items"])

            df_results = pd.concat([df_results, df_page], ignore_index=True)

        return df_results


def make_post_request(payload, headers):
    """Makes a post request to the aoe 4 ladder api"""

    api_url = "https://api.ageofempires.com/api/ageiv/Leaderboard"

    r = requests.post(api_url, json=payload, headers=headers)
    return r.json(), r.status_code


if __name__ == "__main__":
    # This probably could be different
    aoe4_connection = APIConnection()
    results = aoe4_connection.get_all_data()
    print(results.tail())
