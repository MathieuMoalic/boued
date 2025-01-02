import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.router.categories import router as categories_router
from backend.router.items import router as items_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("database")


app = FastAPI()


# Mount static files
app.mount("/static", StaticFiles(directory="./static"), name="static")

# Include routes
app.include_router(items_router)
app.include_router(categories_router)


# handle all ValueErrors
@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )
