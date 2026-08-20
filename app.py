from fastapi import FastAPI
from src.api.routes import router
app=FastAPI(title='Outreach Multi-Agent', version='1.0.0', docs_url=None, redoc_url=None)
app.include_router(router)
