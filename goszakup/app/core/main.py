from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import base
from .config import clear_envs
from .logger import CustomLogger


app = FastAPI(
    title="Egov Parsers",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
app.logger = CustomLogger().set_logger()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(base.router)


@app.on_event("startup")
async def startup():
    clear_envs()


@app.get("/healthcheck/")
def root():
    return {"status": "Egov parsers is OK"}
