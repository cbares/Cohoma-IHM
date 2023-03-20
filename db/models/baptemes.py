from sqlalchemy import Column,Integer, String,Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class Bapteme(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    marker_id = Column(Integer, ForeignKey("marker.id"))
    marker = relationship("Marker", back_populates="terrain")
