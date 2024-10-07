from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime

from db.base_class import Base


class Satellite(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    timestamp = Column(DateTime)
    longitude = Column(Float)
    latitude = Column(Float)
    altitude = Column(Float)
    homing = Column(Float)
    speed = Column(Float)
    battery = Column(Float)
