""" This module creates the schema to hold the data from the AoE 4 API """

import sqlite3 as sql
import os

def create_database(name:str) -> None:
    """ Creates the sqlite database """

    con = sql.connect(name)
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE elo
    (
        gameId integer,
        userId integer,
        rlUserId integer,
        userName text,
        avatarUrl text,
        playerNumber integer,
        elo integer,
        eloRating integer,
        rank integer,
        region integer,
        wins integer,
        winPercent real,
        losses integer,
        winStreak integer
    )
    """)
    con.commit()
    con.close()

if __name__ == "__main__":
    db_name = 'aoe4elo.db'
    try:
        os.remove(db_name)
    except FileNotFoundError:
        pass
    create_database(db_name)
