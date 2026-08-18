from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Product, OrderItem
from app.repository import products as products_repository
from app.schemas.products import (
	CategoryResponse,
	ProductResponse,
	ProductCreateRequest,
	ProductUpdateRequest,
)


def create_category(db: Session, name: str, slug: str, parent_id: int | None) -> CategoryResponse:
	if products_repository.get_category_by_slug(db, slug):
		raise HTTPException(status_code=400, detail=f"Category with slug '{slug}' already exists")
	if parent_id is not None and not products_repository.get_category_by_id(db, parent_id):
		raise HTTPException(status_code=404, detail=f"Parent category {parent_id} not found")
	category = products_repository.create_category(db, name, slug, parent_id)
	return CategoryResponse.model_validate(category)


def list_categories(db: Session) -> list[CategoryResponse]:
	categories = products_repository.get_all_categories(db)
	return [CategoryResponse.model_validate(c) for c in categories]

def create_product(db: Session, payload: ProductCreateRequest) -> ProductResponse:
	if products_repository.get_product_by_slug(db, payload.slug):
		raise HTTPException(status_code=400, detail=f"Product with slug '{payload.slug}' already exists")
	if not products_repository.get_category_by_id(db, payload.category_id):
		raise HTTPException(status_code=404, detail=f"Category {payload.category_id} not found")

	product = products_repository.create_product(db, **payload.model_dump())
	return ProductResponse.model_validate(product)


def get_product(db: Session, product_id: int) -> ProductResponse:
	product = products_repository.get_product_by_id(db, product_id)
	if not product:
		raise HTTPException(status_code=404, detail="Product not found")
	return ProductResponse.model_validate(product)


def list_products(
		db: Session,
		category_id: int | None,
		search: str | None,
		min_price: Decimal | None,
		max_price: Decimal | None,
		page: int,
		page_size: int,
) -> dict:
	offset = (page - 1) * page_size
	items = products_repository.list_products(
		db, category_id=category_id, search=search,
		min_price=min_price, max_price=max_price,
		offset=offset, limit=page_size,
	)
	total = products_repository.count_products(
		db, category_id=category_id, search=search,
		min_price=min_price, max_price=max_price,
	)
	return {
		"items": [ProductResponse.model_validate(p) for p in items],
		"total": total,
		"page": page,
		"page_size": page_size,
	}


def update_product(db: Session, product_id: int, payload: ProductUpdateRequest) -> ProductResponse:
	product = products_repository.get_product_by_id(db, product_id)
	if not product:
		raise HTTPException(status_code=404, detail="Product not found")

	updated = products_repository.update_product(db, product, payload.model_dump())
	return ProductResponse.model_validate(updated)


def delete_product(db: Session, product_id: int) -> None:
	product = products_repository.get_product_by_id(db, product_id)
	if not product:
		raise HTTPException(status_code=404, detail="Product not found")

	was_ever_ordered = db.query(OrderItem).filter(OrderItem.product_id == product_id).first() is not None

	if was_ever_ordered:
		products_repository.update_product(db, product, {"is_active": False})
		raise HTTPException(
			status_code=409,
			detail="Product has order history and cannot be deleted — it has been deactivated instead",
		)

	products_repository.delete_product(db, product)