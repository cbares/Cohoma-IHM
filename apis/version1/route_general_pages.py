from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from core.map_layers import get_map_layers

templates = Jinja2Templates(directory="templates")
general_pages_router = APIRouter()

FRILEUSE = ((48.8645, 1.89201),  16)
ENSEA = ((49.039, 2.072), 18)
ORIGIN = FRILEUSE


@general_pages_router.get("/")
async def home(request: Request):
    leafmap = get_map_layers(*ORIGIN)
    context = { "request": request }
    context.update(leafmap)
    return templates.TemplateResponse("general_pages/homepage.html", context=context)


@general_pages_router.get('/favicon.ico', response_class=RedirectResponse, status_code=302)
def favicon():
    return 'static/favicon.ico'
