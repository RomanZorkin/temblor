from pydantic import BaseModel


class RequestParam(BaseModel):
    format: str = 'geojson'
    starttime: str = '2023-06-18'
    endtime: str = '2023-06-20'
    minlatitude: str = '41.162'
    maxlatitude: str = '81.957'
    minlongitude: str = '19.688'
    maxlongitude: str = '190.547'
    minmagnitude: str = '2.5'


class RequestConfig(BaseModel):

    endpoint = 'https://earthquake.usgs.gov/fdsnws/event/1/query'
    params: RequestParam = RequestParam()
    timeout: float = 10.0


areas = {
    'russia': {
        'minlatitude': '41.162',
        'maxlatitude': '81.957',
        'minlongitude': '19.688',
        'maxlongitude': '190.547',
        'minmagnitude': '2.5',
    },
}