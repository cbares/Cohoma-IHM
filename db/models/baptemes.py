from sqlalchemy import Column, Integer, String, Float

from db.base_class import Base


class Bapteme(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    longitude = Column(Float)
    latitude = Column(Float)
    type = Column(String, nullable=False)
