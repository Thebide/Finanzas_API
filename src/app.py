from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.route import api_router
from .config.logger import config_loggin
from .database import db_connection 


@asynccontextmanager
async def lifespan(application: FastAPI):
    # Antes de levantar el servidor
    config_loggin()
    db_connection.connect()
    yield
    db_connection.disconnect()
    # Antes de cerrar el servidor

application = FastAPI(description="Proyecto de finanzas personales en python+fastapi",
                      version="0.0.0",
                      title="Finanzas personales",
                      lifespan=lifespan,
                      )

application.include_router(api_router)