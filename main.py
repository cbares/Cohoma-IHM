import csv
import os.path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.config import settings
from apis.base import api_router
from db.repository.baptemes import create_new_bapteme
from db.session import engine, get_db
from db.base import Base
from schemas.baptemes import BaptemeCreate


def include_router(app):
    app.include_router(api_router)


def configure_static(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")


def create_tables():
    print("Create tables")
    Base.metadata.create_all(bind=engine)


# conversion: https://geofree.fr/gf/coordinateconv.asp#listSys UTM31 => GPS
def load_terrain():
    points = []
    with open(settings.TERRAIN, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            point = (float(row['Lng']), float(row['Lat']))
            point = BaptemeCreate(name=row['Nom'],type=row['type'],longitude=row['Lng'],latitude=row['Lat'])
            db = next(get_db())
            mark = create_new_bapteme(point, db)
            points.append(points)
    print(points)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    configure_static(app)
    db_file = settings.DATABASE_URL.split('/')[-1]
    if not os.path.exists(db_file):
        create_tables()
        load_terrain()
    return app


fast_app = start_application()
