from datetime import datetime

from pydantic import BaseModel

from db.models.satellites import Satellite


class SatelliteCreate(BaseModel):
    name: str
    timestamp: datetime | None
    longitude: float
    latitude: float
    altitude: float | None
    homing: float | None
    speed: float | None
    battery: float | None


class ShowSatellite(BaseModel):
    id: int
    name: str
    timestamp: datetime
    longitude: float
    latitude: float
    altitude: float | None
    homing: float | None
    speed: float | None
    battery: float | None

    class Config:  # tells pydantic to convert even non dict obj to json
        orm_mode = True


class Geolocation(BaseModel):
    longitude: float
    latitude: float

    class Config:  # tells pydantic to convert even non dict obj to json
        orm_mode = True


class ReportSatellite(BaseModel):
    team: str = "Theseus"
    auth: str = "key"
    source: str
    geolocation: Geolocation
    altitude: float = 0
    timestamp: int

    def __init__(self, m: Satellite = None, **kwargs):
        if m:
            geolocation = Geolocation(latitude=m.latitude, longitude=m.longitude)
            super().__init__(geolocation=geolocation, source=m.name, timestamp=int(m.timestamp.timestamp() * 1000))
        else:
            super().__init__(**kwargs)

    class Config:  # tells pydantic to convert even non dict obj to json
        orm_mode = True
