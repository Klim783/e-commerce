
from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependency import get_db, require_admin
from app.models import User
from app.schemas.products import ProductCreateRequest, ProductUpdateRequest, ProductResponse
from app.services import products as products_service
from app.schemas.products import ProductFilterParams, PaginatedProductsResponse
from app.services import products as product_service
router = APIRouter()


@router.get("/products")
def list_products(
		db: Session = Depends(get_db),
		category_id: int | None = Query(None),
		search: str | None = Query(None, description="Поиск по названию товара"),
		min_price: Decimal | None = Query(None),
		max_price: Decimal | None = Query(None),
		page: int = Query(1, ge=1),
		page_size: int = Query(20, ge=1, le=100),
):
	return products_service.list_products(
		db, category_id, search, min_price, max_price, page, page_size
	)


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
	return products_service.get_product(db, product_id)


@router.post("/products", response_model=ProductResponse)
def create_product(
		payload: ProductCreateRequest,
		db: Session = Depends(get_db),
		admin: User = Depends(require_admin),
):
	return products_service.create_product(db, payload)


@router.patch("/products/{product_id}", response_model=ProductResponse)
def update_product(
		product_id: int,
		payload: ProductUpdateRequest,
		db: Session = Depends(get_db),
		admin: User = Depends(require_admin),
):
	return products_service.update_product(db, product_id, payload)


@router.delete("/products/{product_id}", status_code=204)
def delete_product(
		product_id: int,
		db: Session = Depends(get_db),
		admin: User = Depends(require_admin),
):
	products_service.delete_product(db, product_id)

@router.get("/search", response_model=PaginatedProductsResponse)
def search_products(
	params:ProductFilterParams = Depends(),
	db:Session = Depends(get_db)
):
	return products_service.search_products(db, params)
