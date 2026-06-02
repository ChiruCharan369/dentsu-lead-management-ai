from fastapi import FastAPI
from app.routes.icp_route import router as icp_router
from app.db.cache_db import init_db
from app.routes.translator_route import router as translator_router
from app.routes.file_convert_route import router as file_convert_router

app = FastAPI()

init_db()

app.include_router(icp_router)
app.include_router(translator_router)
app.include_router(file_convert_router)

@app.get("/")
def health_check():
    return {"status": "running"}