from fastapi import FastAPI

from app.core.startup.lifespan import lifespan
from app.routes import router

app = FastAPI(lifespan=lifespan, title="T2G APIs")

api_prefix = "/shorten"

app.include_router(router=router, prefix=api_prefix)