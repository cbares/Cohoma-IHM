import json
from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.websockets import ConnectionManager
from db.repository.satellites import list_last_position_satellites, retrieve_satellite_by_id, names_satellites, \
    retrieve_satellite_by_name, list_report_satellites, list_satellites, create_new_satellite
from db.session import get_db
from schemas.satellites import ReportSatellite, ShowSatellite, SatelliteCreate

router = APIRouter()
manager = ConnectionManager()


@router.post("/", response_model=ShowSatellite, status_code=status.HTTP_201_CREATED)
async def create_satellite(satellite: SatelliteCreate, db: Session = Depends(get_db)):
    """Create a new satellite position"""
    new_position = create_new_satellite(satellite=satellite, db=db)
    await manager.broadcast(ShowSatellite(**new_position.__dict__).model_dump_json())
    return new_position


@router.get("/path/{name}", response_model=List[ShowSatellite], response_model_by_alias=False)
def read_satellite_path(name: str, db: Session = Depends(get_db)):
    """Retrieve all positions for a satellite"""
    marker = retrieve_satellite_by_name(name=name, db=db)
    if not marker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Marker with this id ({id}) does not exist")
    return marker


@router.get("/names", response_model=List[str], response_model_by_alias=False)
def get_satellites_names(db: Session = Depends(get_db)):
    """Retrieve all satellite's names

    Returns:
    - **list**: A list of string of all satellite's names.
    """
    markers = names_satellites(db=db)
    return markers


@router.get("/all", response_model=List[ShowSatellite], response_model_by_alias=False)
def dump_satellites_table(db: Session = Depends(get_db)):
    """Dump all satellite table"""
    markers = list_satellites(db=db)
    return markers


@router.get("/reporting", response_model=List[ReportSatellite], response_model_by_alias=False)
def get_satellites_last_pos_for_reporting(db: Session = Depends(get_db)):
    """Retrieve last position of all Satellites, for ODAC reporting

    Returns:
    - **list**: A list of the last position of all satellites in ODAC Format.
    """
    markers = list_report_satellites(db=db)
    return markers


@router.get("/last", response_model=List[ShowSatellite], response_model_by_alias=False)
def get_satellites_last_pos(db: Session = Depends(get_db)):
    """Retrieve last position of all satellites.

     Returns:
    - **list**: A list of the last position of all satellites.
    """
    markers = list_last_position_satellites(db=db)
    return markers


@router.get("/{id}", response_model=ShowSatellite, response_model_by_alias=False)
def get_satelitte_entry(id: int, db: Session = Depends(get_db)):
    """Retrieve one satellite position"""
    marker = retrieve_satellite_by_id(id=id, db=db)
    if not marker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Marker with this id ({id}) does not exist")
    return marker
