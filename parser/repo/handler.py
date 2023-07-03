from datetime import datetime

import pandas as pd

from parser.db import client


def show_tables():
    result = client.command("""SHOW TABLES FROM quake""")
    return result


def upload_df(frame: pd.DataFrame, table: str = 'quakes') -> bool:
    result = client.insert_df(table, frame)
    print(result)
    return True


def get_last_datetime() -> datetime:
    tmp_query = client.query_df("""SELECT max(Date) as last FROM quakes""")
    return tmp_query['last'].values[0].astype('M8[ms]').astype('O')


def col_filter(table: str, col: str, scores: float):
    tmp_query = client.query_df(f"""SELECT *
    FROM {table}
    WHERE {col} > {scores}
    """)
    return tmp_query


def col_filter_diapason(table: str, col: str, start: tuple, end: float, ) -> pd.DataFrame:
    tmp_query = client.query_df(f"""SELECT *
    FROM {table}
    WHERE {col} > {start} AND {col} < {end}
    """)
    return tmp_query
