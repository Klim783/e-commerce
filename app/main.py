from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import router as auth_router
from app.api.v1.Categories import router as categories_router
from app.api.v1.products import router as products_router
from app.api.v1.cart import router as cart_router
from app.api.v1.orders import router as orders_router
from app.api.v1.reviews import router as reviews_router
from app.api.v1.wishlist import router as wishlist_router

app = FastAPI(title="E-commerce API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(categories_router, prefix="/api/v1", tags=["categories"])
app.include_router(products_router, prefix="/api/v1", tags=["products"])
app.include_router(cart_router, prefix="/api/v1", tags=["cart"])
app.include_router(orders_router, prefix="/api/v1", tags=["orders"])
app.include_router(reviews_router, prefix="/api/v1", tags=["reviews"])
app.include_router(wishlist_router, prefix="/api/v1", tags=["wishlist"])


@app.get("/health")
def health_check():
    return {"status": "ok"}