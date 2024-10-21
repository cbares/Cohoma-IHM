from datetime import datetime

from pydantic import BaseModel, Field

from db.models.satellites import Satellite


class SatelliteCreate(BaseModel):
    name: str = Field(title="Name of the satellite")
    timestamp: datetime | None = Field(title="Timestamp of the position")
    longitude: float = Field(title="Longitude of the satellite")
    latitude: float = Field(title="Latitude of the satellite")
    altitude: float | None = Field(title="Altitude of the satellite")
    homing: float | None = Field(title="Homing of the satellite")
    speed: float | None = Field(title="Speed of the satellite")
    battery: float | None = Field(title="Battery of the satellite")


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
        from_attributes = True


class Geolocation(BaseModel):
    longitude: float
    latitude: float

    class Config:  # tells pydantic to convert even non dict obj to json
        from_attributes = True


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
        from_attributes = True
