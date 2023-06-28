from datetime import datetime
from pathlib import Path

import pandas as pd

from planet.app import Planet
from parser.extractor.handler import QuakeExtractor
from parser.repo import handler


class QuakeParser:

    def __init__(self, start: datetime, end: datetime, area: str) -> None:
        self.start = start
        self.end = end
        self.area = area
        self.quakes = QuakeExtractor(self.start, self.end)
        self.quake_df = pd.DataFrame()
        self.make_frame()

    def planet_param(self, row) -> None:
        planet = Planet(row['Долгота'], row['Широта'], row['Дата'])
        return pd.concat([row, pd.Series(planet.get_parameters())])

    def make_frame(self) -> None:
        self.quakes.period_list
        self.quakes.remote_extract(self.area)
        self.quake_df = self.quakes.to_frame()
        self.quake_df.columns = ['Магнитуда', 'Долгота', 'Широта', 'Дата']
        self.quake_df = self.quake_df.apply(self.planet_param, axis=1)


class CsvParser(QuakeParser):

    def __init__(self, start: datetime, end: datetime, area: str, filename: str) -> None:
        super().__init__(start, end, area)
        self.filename = filename
        self.data_path = Path('data')

    def to_csv(self) -> bool:
        csv_file = self.data_path / f'{self.filename}.csv'
        self.quake_df.to_csv(csv_file)
        return True


class ClickHouseParser(QuakeParser):

    def __init__(self, start: datetime, end: datetime, area: str) -> None:
        super().__init__(start, end, area)

    def upload_quakes(self) -> None:
        tmp_df = self.quake_df.copy()
        tmp_columns = tmp_df.columns.to_list()
        tmp_columns[0] = 'Magnitude'
        tmp_columns[1] = 'Longitude'
        tmp_columns[2] = 'Latitude'
        tmp_columns[3] = 'Date'
        tmp_df.columns = tmp_columns
        handler.upload_df(tmp_df)
