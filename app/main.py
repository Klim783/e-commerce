from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import router as auth_router
from app.api.v1.Categories import router as categories_router
from app.api.v1.products import router as products_router

app = FastAPI(title="E-commerce API")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"]
)

app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(categories_router, prefix="/api/v1", tags=["categories"])
app.include_router(products_router, prefix="/api/v1", tags=["products"])


@app.get("/health")
def health_check():
	return {"status": "ok"}
