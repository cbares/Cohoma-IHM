import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from schemas.markers import MarkerCreate, MarkerUpdate, ReportMarker, Geolocation
from db.models.markers import Marker


def create_new_marker(marker:MarkerCreate, db:Session):
    mark = Marker(name=marker.waypoint,
        timestamp=datetime.datetime.now(),
        longitude=marker.lng,
        latitude=marker.lat
        )
    db.add(mark)
    db.commit()
    db.refresh(mark)
    return mark


def _retrieve_marker(id: int, db: Session):
    existing_marker = db.query(Marker).filter(Marker.id==id)
    if not existing_marker.first():
        raise NotFoundException
    return existing_marker


def retrieve_marker(id: int, db: Session):
    existing_marker = _retrieve_marker(id, db).first()
    return existing_marker


def list_markers(db:Session):
    items = db.query(Marker).all()
    return items


def list_report_markers(db:Session):
    items = db.query(Marker.id, Marker.name,
                     Marker.latitude, Marker.longitude,
                     Marker.timestamp, func.max(Marker.timestamp))\
        .group_by(Marker.name)
    reports = []
    for i in items:
        rm = ReportMarker(i)
        reports.append(rm)
    return reports


def delete_marker_by_id(id: int, db: Session):
    existing_marker = _retrieve_marker(id, db)
    if existing_marker.first().is_locked:
        raise LockedException
    existing_marker.delete(synchronize_session=False)
    db.commit()


def update_marker_by_id(id: int, item: MarkerUpdate, db: Session):
    stored_marker = _retrieve_marker(id, db).first()
    update_data = item.dict(exclude_unset=True)
    print("item", item)
    print("update", update_data)
    #updated_item = stored_marker.copy(update=update_data)
    print("marker", stored_marker.__dict__)
    #stored_marker.__dict__.update(update_data)
    stored_marker.latitude = update_data['latitude']
    stored_marker.longitude = update_data['longitude']
    print("marker", stored_marker.__dict__)
    db.commit()
    return stored_marker


class NotFoundException(Exception):
    pass


class LockedException(Exception):
    pass
