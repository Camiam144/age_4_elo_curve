import json
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


class APIConnection():
    """ Makes the connection to the AoE 4 API """
    def __init__(self) -> None:

        self.api_url = "https://api.ageofempires.com/api/ageiv/Leaderboard"
        self.headers = {"content-type":"application/json",
                        "Accept" : "application/json"
                        }

    def _make_post_request(self, payload):
        r = requests.post(self.api_url, json=payload, headers=self.headers)
        return r.json

    def get_all_data(self):
        count_per_page = 100
        payload = {
            "region":7,
            "versus":"players",
            "matchType":"unranked",
            "teamSize":"1v1",
            "searchPlayer":"",
            "page":"1",
            "count":str(count_per_page)
            }

        first_request = self._make_post_request(payload)
        total_players = first_request['count']
        total_pages = math.ceil(total_players/count_per_page)

        df_results = pd.DataFrame(data=first_request['items'])

        return df_results

def make_post_request(payload, headers):
    """ Makes a post request to the aoe 4 ladder api """

    api_url = "https://api.ageofempires.com/api/ageiv/Leaderboard"

    r = requests.post(api_url, json=payload, headers=headers)
    return r.json(), r.status_code


if __name__ == "__main__":

    count_per_page = 100

    payload = {
        "region":7,
        "versus":"players",
        "matchType":"unranked",
        "teamSize":"1v1",
        "searchPlayer":"",
        "page":"1",
        "count":str(count_per_page)
        }

    headers = {"content-type":"application/json",
            "Accept" : "application/json"
            }

    data, status = make_post_request(payload, headers)

    total_players = data['count']
    total_pages = math.ceil(total_players / count_per_page)