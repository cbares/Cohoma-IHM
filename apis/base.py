from fastapi import APIRouter

from apis.version1 import route_general_pages
from apis.version1 import route_markers
from apis.version1 import route_baptemes


api_router = APIRouter()
api_router.include_router(route_general_pages.general_pages_router, prefix="", tags=["general_pages"])
api_router.include_router(route_markers.router, prefix="/api/waypoint", tags=["markers"])
api_router.include_router(route_baptemes.router, prefix="/api/baptemes", tags=["baptemes"])
