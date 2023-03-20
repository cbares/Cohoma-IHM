from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.markers import MarkerCreate, ShowMarker, MarkerUpdate
from db.session import get_db
from db.repository.markers import create_new_marker, retrieve_marker, list_markers, delete_marker_by_id, \
    NotFoundException, LockedException, update_marker_by_id

router = APIRouter()


@router.post("/", response_model = ShowMarker, status_code=status.HTTP_201_CREATED)
def create_marker(marker : MarkerCreate, db: Session = Depends(get_db)):
    mark = create_new_marker(marker=marker, db=db)
    return mark


@router.get("/get/{id}", response_model=ShowMarker, response_model_by_alias=False)
def read_marker(id:int, db:Session = Depends(get_db)):
    marker = retrieve_marker(id=id, db=db)
    if not marker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Marker with this id ({id}) does not exist")
    return marker


@router.get("/all",response_model=List[ShowMarker], response_model_by_alias=False)
def read_markers(db:Session = Depends(get_db)):
    markers = list_markers(db=db)
    return markers


@router.delete("/delete/{id}")
def delete_marker(id: int, db: Session = Depends(get_db)):
    try:
        delete_marker_by_id(id=id, db=db)
    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Marker with id {id} not found")
    except LockedException:
        raise HTTPException(status_code=status.HTTP_423_LOCKED,
                            detail=f"Marker with id {id} is locked")
    return {"msg": "Successfully deleted."}


@router.patch("/update/{id}", response_model = ShowMarker)
def update_marker(id: int, item: MarkerUpdate, db: Session = Depends(get_db)):
    try:
        marker = update_marker_by_id(id=id, item=item, db=db)
    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Marker with this id ({id}) does not exist")
    return marker
