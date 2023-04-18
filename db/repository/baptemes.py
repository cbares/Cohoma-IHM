from sqlalchemy.orm import Session

from db.models.baptemes import Bapteme
from schemas.baptemes import BaptemeCreate, NameBapteme


def create_new_bapteme(marker:BaptemeCreate, db:Session):
    mark = Bapteme(
        name=marker.name,
        type=marker.type,
        longitude=marker.longitude,
        latitude=marker.latitude
        )
    db.add(mark)
    db.commit()
    db.refresh(mark)
    return mark


def list_baptemes(db:Session):
    items = db.query(Bapteme).all()
    return items


def names_baptemes(db:Session):
    items = db.query(Bapteme.name).distinct()
    return [i.name for i in items]


def filter_baptemes(name: str, db: Session):
    items = db.query(Bapteme).filter_by(name=name).all()
    return items


def points_baptemes(db: Session):
    items = db.query(Bapteme).filter_by(type="point").all()
    return items
