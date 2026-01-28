from fastapi import FastAPI

from app.lifespan import lifespan
from app.routers import router 

app = FastAPI(lifespan=lifespan, title="T2G APIs")

api_prefix = "/shorten"

app.include_router(router=router, prefix=api_prefix)