from fastapi import FastAPI
from starlette.requests import Request

from application.routers import upload


app = FastAPI()
app.include_router(upload.router)