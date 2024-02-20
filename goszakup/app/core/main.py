from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import base
from .logger import CustomLogger


async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Goszakup",
    version="2.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan,
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


@app.get("/healthcheck/")
def root():
    return {"status": "Egov parsers is OK"}
