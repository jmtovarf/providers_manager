from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from api import templates, _l

user = APIRouter()


@user.get("/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, **_l})
