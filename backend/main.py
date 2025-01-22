import logging
import os
from pathlib import Path

from fastapi import Depends, FastAPI, Request, WebSocket
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles

from backend.jwt import jwt_login
from backend.router.categories import router as categories_router
from backend.router.items import router as items_router
from backend.websocket import handle_websocket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("database")


app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await handle_websocket(websocket)


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return jwt_login(form_data.username, form_data.password)


app.include_router(items_router)
app.include_router(categories_router)


# handle all ValueErrors
@app.exception_handler(ValueError)
async def value_error_exception_handler(_: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


# This must be the last route
static_path = os.path.dirname(os.path.abspath(__file__)) + "/static"
if Path(static_path).exists():
    app.mount(
        "/",
        StaticFiles(directory=static_path, html=True),
        name="static",
    )
else:
    logger.warning("No static files directory found")
