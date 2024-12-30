import logging

from fastapi import FastAPI
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
