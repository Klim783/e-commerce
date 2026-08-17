from decimal import Decimal

from sqlalchemy.orm import Session
from app.models import Category, Product

def get_category_by_slug(db:Session, slug:str) -> Category|None:
	return db.query(Category).filter(Category.slug == slug).first()

def get_category_by_id(db:Session, id:int) -> Category|None:
	return db.query(Category).filter(Category.id == id).first()

def get_all_categories(db:Session) ->list[Category]:
	return db.query(Category).all()

def create_category(db:Session, slug:str, name:str, parent_id:str|None) -> Category|None:
	category = Category(name = name, slug = slug, parent_id = parent_id)
	db.add(category)
	db.commit()
	db.refresh(category)
	return category


def get_product_by_id(db:Session, product_id:int) -> Product|None:
	return db.query(Product).filter(Product.id == product_id).first()

def get_product_by_slug(db:Session, slug:str) -> Product|None:
	return db.query(Product).filter(Product.slug == slug).first()

def list_products(
		db:Session,
		category_id:int|None = None,
		search:str|None = None,
		min_price:Decimal|None = None,
		max_price:Decimal|None = None,
		only_active:bool = True,
		offset:int = 0,
		limit:int = 20,
) -> list[Product]:
	query = db.query(Product)

	if only_active:
		query = query.filter(Product.is_active.is_(True))
		if category_id is not None:
			query = query.filter(Product.id == category_id)
		if search:
			query = query.filter(Product.name.ilike(f"%{search}%"))
		if min_price is not None:
			query = query.filter(Product.price >= min_price)
		if max_price is not None:
			query = query.filter(Product.price <= max_price)
		return query.order_by(Product.created_at.desc()).offset(offset).limit(limit).all()


def create_products(db:Session, **fields) -> Product:
	product = Product(**fields)
	db.add(product)
	db.commit()
	db.refresh(product)
	return product

def update_products(db:Session, product:Product, fields:dict) -> Product:
	for key,value in fields.items():
		if value is not None:
			setattr(product, key, value)
		db.commit()
		db.refresh(product)
		return product

def delete_product(db:Session, product:Product) -> None:
	db.delete(product)
	db.commit()
