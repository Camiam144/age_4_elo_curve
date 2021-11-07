""" This module pulls the data from the aoe4 api and saves it to the sqlite database """

import sqlite3 as sql
from datetime import datetime

import pandas as pd

from api_connection import APIConnection


def pull_data() -> pd.DataFrame:
    """Pulls the data from the aoe4 api"""

    aoe4_api_conn = APIConnection()
    data = aoe4_api_conn.get_all_data()

    return data


if __name__ == "__main__":

    data = pull_data()

    timestamp = datetime.now()
    data["load_time"] = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    db_name = "aoe4elo.db"
    table_name = "elo"
    with sql.connect(db_name) as conn:
        data.to_sql(table_name, conn, if_exists="append", index=False)
