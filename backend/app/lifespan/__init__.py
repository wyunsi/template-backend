from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.license.manager import license_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await license_manager.activate()
    license_manager.start_heartbeat()
    yield
    await license_manager.stop()
