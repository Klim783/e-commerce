from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import CartItem
from app.models import Product



def get_cart_items(db:Session, user_id:int) ->list[CartItem]:
	stmt = select(CartItem).where(CartItem.user_id == user_id)
	return db.execute(stmt).scalars().all()

def get_cart_item(db:Session, user_id:int, product_id:int) -> CartItem|None:
	stmt = select(CartItem).where(
		CartItem.user_id == user_id,
		CartItem.product_id == product_id
	)
	return db.execute(stmt).scalar_one_or_none()

def get_product(db:Session, product_id:int) -> Product|None:
	return db.get(Product, product_id)

def create_cart_item(db:Session, user_id:int, product_id:int, quantity:int) -> CartItem:
	item = CartItem(user_id = user_id, product_id = product_id, quantity = quantity)
	db.add(item)
	db.commit()
	db.refresh(item)
	return item

def update_cart_item_quantity(db:Session, item:CartItem, quantity:int) -> CartItem:
	item.quantity = quantity
	db.commit()
	db.refresh(item)
	return item

def delete_cart(db:Session, user_id:int) -> None:
	items = get_cart_item(db, user_id)
	for item in items:
		db.delete(item)
	db.commit()