from fastapi import FastAPI, Request

from . import views

app = FastAPI()

app.include_router(views.router)
