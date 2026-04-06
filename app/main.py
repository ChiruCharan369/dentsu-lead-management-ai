from fastapi import FastAPI
from app.routes.icp_route import router as icp_router
from app.db.cache_db import init_db

app = FastAPI()

init_db()

app.include_router(icp_router)


@app.get("/")
def root():
    return {"status": "running"}