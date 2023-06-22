from datetime import datetime

import httpx

from parser import config
from parser.schemas import QuakeRequest, QuakeRequestList


config_app = config.RequestConfig()


def get_rows():
    request = httpx.get(config_app.endpoint, params=config_app.params.dict(), timeout=config_app.timeout)
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
