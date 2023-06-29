from datetime import datetime

import pandas as pd

from parser.db import client


def show_tables():
    result = client.command("""SHOW TABLES FROM quake""")
    return result


def upload_df(frame: pd.DataFrame) -> bool:
    result = client.insert_df('quakes', frame)
    print(result)
    return True


def get_last_datetime() -> datetime:
    tmp_query = client.query_df("""SELECT max(Date) as last FROM quakes""")
    return tmp_query['last'].values[0].astype('M8[ms]').astype('O')
