import uvicorn

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from settings import PORT, RELOAD, SECRET_KEY

from api.models import create_db_models
from api.routes.user import user

import docs

create_db_models()

app = FastAPI(
    title=docs.__title__,
    description=docs.__description__,
    version=docs.__version__,
    openapi_tags=docs.__tags_metadata__,
)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.mount("/static", StaticFiles(directory="client/static"), name="static")


@app.middleware("http")
async def add_api_version(request: Request, call_next):
    request.state.api_version = docs.__api_version__
    response = await call_next(request)
    return response


app.include_router(user, prefix=docs.__api_version__)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, reload=RELOAD)
