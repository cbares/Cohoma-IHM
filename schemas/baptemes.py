from pydantic import BaseModel


class BaptemeCreate(BaseModel):
    name: str
    type: str
    longitude: float
    latitude: float


class ShowBapteme(BaseModel):
    id: int
    name: str
    longitude: float
    latitude: float
    type: str

    class Config:  # tells pydantic to convert even non dict obj to json
        from_attributes = True


class NameBapteme(BaseModel):
    name: str

    class Config:  # tells pydantic to convert even non dict obj to json
        from_attributes = True