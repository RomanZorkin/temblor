from datetime import datetime
from typing import List, Tuple

import httpx

from parser.config import RequestConfig
from parser.schemas import QuakeRequest, QuakeRequestList


class QuakeExtractor:
    """Класс отвечает за парсинг данных и передачу их далее в базу даных или csv файл."""

    def __init__(self, start_date: datetime, end_date: datetime) -> None:
        self.start = start_date
        self.end = end_date
        self.period_list: List[Tuple[datetime, datetime]] = []
        self.quake_list = []
        self._period_slices()

    def remote_extract(self):
        for period in self.period_list:
            config = self._get_param(period)
            api_data = self._read_api(config)
            self.quake_list.extend(api_data.rows)            

    def _get_param(self, period: Tuple[datetime, datetime]) -> RequestConfig:
        start_date, end_date = period
        config = RequestConfig()
        config.params.starttime = start_date.strftime('%Y-%m-%d')
        config.params.endtime = end_date.strftime('%Y-%m-%d')
        return config

    def _read_api(self, remote_conf: RequestConfig) -> QuakeRequestList:
        request = httpx.get(
            remote_conf.endpoint, params=remote_conf.params.dict(), timeout=remote_conf.timeout,
        )
        data = request.json()
        export_list = []

        for row in data['features']:
            export_list.append(
                QuakeRequest(
                    magnitude=row['properties']['mag'],
                    longitude=row['geometry']['coordinates'][0],
                    latitude=row['geometry']['coordinates'][1],
                    date=datetime.fromtimestamp(int(row['properties']['time'] / 1000))
                )
            )

        return QuakeRequestList(rows=export_list)

    def _period_slices(self) -> None:
        current_year = self.start.year
        while current_year < self.end.year + 1:

            if current_year == self.start.year:
                start_period = self.start
                if current_year == self.end.year:
                    end_period = self.end
                else:
                    end_period = datetime(current_year, 12, 31)
                self.period_list.append((start_period, end_period))
                current_year += 1
                continue

            if current_year == self.end.year:
                start_period = datetime(current_year, 1, 1)
                end_period = self.end
                self.period_list.append((start_period, end_period))
                current_year += 1
                continue

            start_period = datetime(current_year, 1, 1)
            end_period = datetime(current_year, 12, 31)
            self.period_list.append((start_period, end_period))
            current_year += 1
