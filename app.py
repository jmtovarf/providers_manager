from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

from api.routes.user import user

import docs

app = FastAPI(
    title=docs.__title__,
    description=docs.__description__,
    version=docs.__version__,
    openapi_tags=docs.__tags_metadata__,
)


app.mount("/static", StaticFiles(directory="client/static"), name="static")

app.include_router(user)
