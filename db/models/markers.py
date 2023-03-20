from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class Marker(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    timestamp = Column(DateTime)
    longitude = Column(Float)
    latitude = Column(Float)
    is_locked = Column(Boolean(), default=False)
    terrain = relationship("Bapteme", back_populates="marker")
