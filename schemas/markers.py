from datetime import datetime
from pydantic import BaseModel, Field


class MarkerCreate(BaseModel):
    waypoint: str
    lng : float
    lat : float


class ShowMarker(BaseModel):
    id: int
    waypoint: str = Field(..., alias="name")
    longitude: float
    latitude: float
    timestamp: datetime

    class Config():  #tells pydantic to convert even non dict obj to json
        orm_mode = True


class MarkerUpdate(BaseModel):
    waypoint: str | None
    longitude : float | None = Field(alias="lng")
    latitude : float | None = Field(alias="lat")
    timestamp: datetime | None

    class Config():  #tells pydantic to convert even non dict obj to json
        orm_mode = True
