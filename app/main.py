from enum import auto

from IPython.core.release import author_email
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.v1.auth import router as auth_router

app = FastAPI(title = "E-commerce")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

app.include_router(auth_router, prefix = '/api/v1', tags = ['Auth'])


@app.get('/health')
def health_check():
    return{'status':'ok'}