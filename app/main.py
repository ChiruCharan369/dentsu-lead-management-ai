from fastapi import FastAPI
from app.routes.icp_route import router as icp_router

app = FastAPI()

app.include_router(icp_router)


@app.get("/")
def root():
    return {"status": "running"}