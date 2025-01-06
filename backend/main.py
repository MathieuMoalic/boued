import logging
from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles

from backend.jwt import jwt_login
from backend.router.categories import router as categories_router
from backend.router.items import router as items_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("database")


app = FastAPI()


app.include_router(items_router)
app.include_router(categories_router)


if Path("static").exists():
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
else:
    logger.warning("No static files directory found")


# handle all ValueErrors
@app.exception_handler(ValueError)
async def value_error_exception_handler(_: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return jwt_login(form_data.username, form_data.password)
