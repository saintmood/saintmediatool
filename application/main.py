from fastapi import FastAPI
from starlette.requests import Request

from application.routers import upload, retrieve


app = FastAPI()
app.include_router(upload.router)
app.include_router(retrieve.router)