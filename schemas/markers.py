from datetime import datetime
from pydantic import BaseModel, Field

from db.models.markers import Marker


class MarkerCreate(BaseModel):
    waypoint: str
    lng: float
    lat: float


class ShowMarker(BaseModel):
    id: int
    waypoint: str = Field(..., alias="name")
    longitude: float
    latitude: float
    timestamp: datetime

    class Config():  # tells pydantic to convert even non dict obj to json
        orm_mode = True


class Geolocation(BaseModel):
    longitude: float
    latitude: float

    class Config():  # tells pydantic to convert even non dict obj to json
        orm_mode = True


class ReportMarker(BaseModel):
    team: str = "Theseus"
    auth: str = "key"
    source: str
    geolocation: Geolocation
    altitude: float = 0
    timestamp: int

    def __init__(self, m:Marker=None, **kwargs):
        if m:
            geolocation = Geolocation(latitude=m.latitude, longitude=m.longitude)
            super().__init__(geolocation=geolocation, source=m.name, timestamp = int(m.timestamp.timestamp() * 1000))
        else:
            super().__init__(**kwargs)

    class Config():  # tells pydantic to convert even non dict obj to json
        orm_mode = True


class MarkerUpdate(BaseModel):
    waypoint: str | None
    longitude : float | None = Field(alias="lng")
    latitude : float | None = Field(alias="lat")
    timestamp: datetime | None

    class Config():  # tells pydantic to convert even non dict obj to json
        orm_mode = True
