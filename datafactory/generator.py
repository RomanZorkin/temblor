import pandas as pd

from parser.repo.handler import col_filter_diapason

enrichment = pd.DataFrame()
count_step = 0


class Enrichment:
    """Класс отвечает за добавление новых однотипных событий в близком гео районе"""

    def __init__(
            self, table: str, column_name: str, magnitude: int, count: int, area: float = 0.5,
    ) -> None:
        self.table = table
        self.column_name = column_name
        self.min_val = magnitude - 1
        self.max_val = magnitude + 1
        self.count = count  # количество доп значений
        self.area = area  # градусы в передалах 50 км. от точки
        self.slicing = self.area / self.count
        self.half_area = self.area / 2

    def enrich(self, quake_series) -> None:
        global enrichment
        if not self.count % 2:
            self.count = self.count + 1
        lat = quake_series['Latitude']  # широта
        lat_list = [
            round((lat - self.half_area) + (self.slicing * step), 3) for step in range(self.count)
        ]
        tmp_df = pd.concat([quake_series.to_frame().T] * self.count, ignore_index=True)
        tmp_df['Latitude'] = lat_list
        enrichment = pd.concat([enrichment, tmp_df], ignore_index=True)

    def start_add(self) -> pd.DataFrame:
        global enrichment
        enrichment = pd.DataFrame()
        tmp_df = col_filter_diapason(self.table, self.column_name, self.min_val, self.max_val)
        tmp_df.apply(self.enrich, axis=1)
        return enrichment
