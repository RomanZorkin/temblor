from datetime import datetime
from typing import List

from pydantic import BaseModel


class QuakeRequest(BaseModel):

    magnitude: float  # магнитуда
    longitude: float   # долгота
    latitude: float  # широта
    date: datetime


class QuakeRequestList(BaseModel):
    rows: List[QuakeRequest]
