from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import OrderStatus
from app.repository import cart as cart_repo
from app.repository import orders as order_repo

def checkout(db:Session, user_id:int):
	cart_items = cart_repo.get_cart_item(db, user_id)
	if not cart_items:
		raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Cart is empty')
	products = {}
	for ci in cart_items:
		product = cart_repo.get_product(db, ci.product_id)
		if product is None or ci.quantity >= product.stock_quantity:
			raise HTTPException(
				status.HTTP_400_BAD_REQUEST,
				f"'{product.name if product else ci.product_id}' no longer has enough stock"
			)
		products[ci.product_id] = product
	try:
		order = order_repo.create_order(db, user_id)
		total = 0
		for ci in cart_items:
			product = product[ci.product_id]
			order_repo.add_order_item(db, order.id, product.id, product.price, ci.quantity)
			order_repo.decrement_stock(db, product, ci.quantity)
			total += product.price * ci.quantity
		order.total = total
		cart_repo.clear_cart(db, user_id)
		db.commit()
		db.refresh(order)
		return order
	except Exception:
		db.rollback()
		raise

def get_order(db:Session, user_id:int, order_id:int):
	order = order_repo.get_order(db, order_id, user_id)
	if order is None:
		raise HTTPException(status.HTTP_404_NOT_FOUND, 'Order not found')
	return order

def list_orders(db:Session, user_id:int):
	return order_repo.get_user_orders(db, user_id)


# ALLOWED_TRANSITIONS = {
# 	"PENDING" : {"PAID", "CANCELLED"},
# 	"PAID": {"SHIPPED","CANCELLED"},
# 	"SHIPPED": {"DELIVERED"},
# 	"DELIVERED": set(),
# 	"CANCELLED" : set(),
# }


ALLOWED_TRANSITIONS: dict[OrderStatus, set[OrderStatus]] = {
    OrderStatus.PENDING: {OrderStatus.PAID, OrderStatus.CANCELLED},
    OrderStatus.PAID: {OrderStatus.SHIPPED, OrderStatus.CANCELLED},
    OrderStatus.SHIPPED: {OrderStatus.DELIVERED},
    OrderStatus.DELIVERED: set(),
    OrderStatus.CANCELLED: set(),
}

def admin_list_orders(db:Session, status:str|None = None):
	return order_repo.get_all_orders(db, status)

def admin_update_order_status(db:Session, order_id:int, new_status:str):
	order = order_repo.get_order_by_id(db, order_id)
	if order is None:
		raise HTTPException(status.HTTP_404_NOT_FOUND, 'Order not found')
	if new_status not in ALLOWED_TRANSITIONS.get(order.status, set()):
		raise HTTPException(
			status.HTTP_400_BAD_REQUEST,
			f'Cannot move order from "{order.status}" to "{new_status}"'
		)
	return order_repo.update_order_status(db, order, new_status)