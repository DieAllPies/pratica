from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# 🏡 Home Page
@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# 🌱 Compostagem Page
@router.get("/compostagem")
def compostagem(request: Request):
    return templates.TemplateResponse("compostagem.html", {"request": request})


# 🌿 Horta Page
@router.get("/horta")
def horta(request: Request):
    return templates.TemplateResponse("horta.html", {"request": request})
