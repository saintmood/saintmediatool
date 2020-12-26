from fastapi import FastAPI
from starlette.requests import Request


app = FastAPI()


@app.get('/ecs/test/')
async def test(request: Request):
    return {'ip': request.client.host}
