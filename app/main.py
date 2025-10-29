from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import pages, sobre

app = FastAPI(title="Portal da Compostagem")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(pages.router)
app.include_router(sobre.router)
