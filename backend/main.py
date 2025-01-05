import logging

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.router.categories import router as categories_router
from backend.router.items import router as items_router
from backend.security import verify_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("database")


app = FastAPI()


app.include_router(items_router)
app.include_router(categories_router)


@app.get("/ping", dependencies=[Depends(verify_password)])
async def pong():
    return {"ping": "pong!"}


app.mount("/", StaticFiles(directory="static", html=True), name="static")


# handle all ValueErrors
@app.exception_handler(ValueError)
async def value_error_exception_handler(_: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )
