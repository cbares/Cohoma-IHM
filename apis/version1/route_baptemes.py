from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.baptemes import ShowBapteme, NameBapteme
from db.session import get_db
from db.repository.baptemes import list_baptemes, names_baptemes, filter_baptemes

from schemas.baptemes import ShowBapteme

router = APIRouter()


@router.get("/", response_model=List[ShowBapteme], response_model_by_alias=False)
def read_markers(db: Session = Depends(get_db)):
    markers = list_baptemes(db=db)
    return markers


@router.get("/names", response_model=List[str], response_model_by_alias=False)
def read_markers(db: Session = Depends(get_db)):
    markers = names_baptemes(db=db)
    return markers


@router.get("/{name}", response_model=List[ShowBapteme], response_model_by_alias=False)
def read_markers(name: str, db: Session = Depends(get_db)):
    markers = filter_baptemes(name=name, db=db)
    return markers


