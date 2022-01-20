from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

from application.routers import upload, retrieve, media
from application.schema import schema


app = FastAPI()
app.include_router(upload.router)
app.include_router(retrieve.router)
app.include_router(media.router)
app.mount("/graphql", GraphQLApp(schema, on_get=make_graphiql_handler()))
