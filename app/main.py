from fastapi import FastAPI
from app.routes.icp_route import router as icp_router
from app.db.cache_db import init_db
from app.routes.translator_route import router as translator_router
from app.routes.intent_route import router as intent_router
from app.routes.extract_route import router as extract_router
from app.routes.language_route import router as language_router
from app.routes.disqualify_route import router as disqualify_router

app = FastAPI()

init_db()

app.include_router(icp_router)
app.include_router(translator_router)
app.include_router(intent_router)
app.include_router(extract_router)
app.include_router(language_router)
app.include_router(disqualify_router)

@app.get("/")
def health_check():
    return {"status": "running"}