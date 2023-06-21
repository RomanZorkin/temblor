from typing import List

from pydantic import BaseModel


class QuakeRequest(BaseModel):

    magnitude: float  # магнитуда
    longitude: str   # долгота
    latitude: str  # широта


class QuakeRequestList(BaseModel):
    rows: List[QuakeRequest]
