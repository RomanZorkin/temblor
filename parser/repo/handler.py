from parser.db import client


def show_tables():
    result = client.command("""SHOW TABLES FROM quake""")
    return result