from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Order, OrderItem
from app.models import Product

def create_order(db:Session, user_id:int) -> Order:
	order = Order(user_id = user_id, status = 'PENDING')
	db.add(order)
	db.flush()
	return order


def add_order_item(db:Session, order_id:int, product_id:int, unit_price, quantity:int):
	item = OrderItem(
		order_id = order_id,
		product_id = product_id,
		unit_price = unit_price,
		quantity = quantity
	)
	db.add(item)
	return item

def decrement_stock(db:Session,product:Product, quantity:int) -> None:
	product.stock_quantity -= quantity
	db.add(product)


def get_order(db:Session, order_id:int, user_id:int) ->Order|None:
	stmt = select(Order).where(Order.id == order_id, Order.user_id == user_id)
	return db.execute(stmt).scalar_one_or_none()

def get_user_orders(db:Session, user_id:int) -> list[Order]:
	stmt = select(Order).where(Order.user_id == user_id).order_by(Order.created_at.desc())
	return db.execute(stmt).scalars().all()


def get_order_by_id(db:Session, order_id:int) -> Order|None:
	return db.get(Order, order_id)

def get_all_orders(db:Session, status:str|None = None) -> list[Order]:
	stmt = select(Order).order_by(Order.created_at.desc())
	if status:
		stmt = stmt.where(Order.status == status)
	return db.execute(stmt).scalars().all()

def update_order_status(db:Session, order:Order, new_status:str) -> Order:
	order.status = new_status
	db.add(order)
	db.commit()
	db.refresh(order)
	return order