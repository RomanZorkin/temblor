from datetime import datetime, timedelta
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
        planet = Planet(row['Longitude'], row['Latitude'], row['Date'])
        return pd.concat([row, pd.Series(planet.get_parameters())])

    def make_frame(self) -> None:
        self.quakes.period_list
        self.quakes.remote_extract(self.area)
        self.quake_df = self.quakes.to_frame()
        self.quake_df.columns = ['Magnitude', 'Longitude', 'Latitude', 'Date']
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

    def __init__(
            self,
            start: datetime = datetime(1990, 1, 1),
            end: datetime = datetime.now(),
            area: str = 'world',
    ) -> None:
        super().__init__(start, end, area)

    def upload_to_bd(self) -> None:
        handler.upload_df(self.quake_df)

    def update_bd(self):
        self.start = handler.get_last_datetime() + timedelta(0, 1)
        self.end = datetime.now()
        self.quakes = QuakeExtractor(self.start, self.end)
        self.make_frame()
        self.upload_to_bd()
        
