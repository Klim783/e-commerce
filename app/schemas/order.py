from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from app.models import OrderStatus

class OrderItemResponse(BaseModel):
	product_id:int
	product_name:str
	unit_price:Decimal
	quantity:int
	subtotal:Decimal

	class Config:
		from_attributes = True


class OrderResponse(BaseModel):
	id :int
	status:OrderStatus
	total:Decimal
	created_at:datetime
	items: list[OrderItemResponse]

	class Config:
		from_attributes = True