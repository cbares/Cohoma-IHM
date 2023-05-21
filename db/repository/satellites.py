import datetime
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from schemas.satellites import SatelliteCreate, ReportSatellite, ShowSatellite
from db.models.satellites import Satellite
from core.config import settings


def create_new_satellite(satellite:SatelliteCreate, db:Session):
    (lng, lat) = settings.ORIGIN[0]
    mark = Satellite(name=satellite.name,
        timestamp=datetime.datetime.now(),
        longitude=satellite.longitude,
        latitude=satellite.latitude,
        altitude=0,
        homing=0,
        speed=0,
        battery=0
        )
    db.add(mark)
    db.commit()
    db.refresh(mark)
    return mark


def _retrieve_satellite(id: int, db: Session):
    existing_satellite = db.query(Satellite).filter(Satellite.id==id)
    if not existing_satellite.first():
        raise ValueError
    return existing_satellite


def retrieve_satellite_by_id(id: int, db: Session):
    existing_satellite = _retrieve_satellite(id, db).first()
    return existing_satellite


def retrieve_satellite_by_name(name: str, db: Session):
    existing_satellite = db.query(Satellite)\
        .filter(Satellite.name == name)\
        .order_by(Satellite.timestamp.desc())

    if not existing_satellite.first():
        raise ValueError
    return existing_satellite.all()


def names_satellites(db: Session):
    items = db.query(Satellite.name).distinct()
    return [i.name for i in items]


def list_satellites(db: Session):
    items = db.query(Satellite).all()
    return items


def _retrieve_last(db: Session):
    items = db.query(Satellite.id, Satellite.name, Satellite.latitude,
                     Satellite.longitude,
                     Satellite.timestamp,
                     func.max(Satellite.timestamp)).group_by(Satellite.name)
    return items


def list_report_satellites(db: Session):
    items = _retrieve_last(db)
    reports = [ReportSatellite(i) for i in items]
    return reports


def list_last_position_satellites(db: Session) -> List[ShowSatellite]:
    return _retrieve_last(db).all()
