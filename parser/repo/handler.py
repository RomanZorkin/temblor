import pandas as pd

from parser.db import client


def show_tables():
    result = client.command("""SHOW TABLES FROM quake""")
    return result


def upload_df(frame: pd.DataFrame) -> bool:
    result = client.insert_df('quakes', frame)
    print(result)
    return True
