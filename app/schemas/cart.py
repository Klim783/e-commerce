from decimal import Decimal

from pydantic import BaseModel, Field, computed_field
from app.schemas.products import ProductResponse

class CartItemAddRequest(BaseModel):
	product_id:int
	quantity:int

class CartItemUpdateRequest(BaseModel):
	quantity:int = Field(..., ge = 1)

class CartItemResponse(BaseModel):
	model_config = {'from_attributes':True}
	id:int
	product: ProductResponse
	quantity: int

	@computed_field
	@property
	def line_total(self) -> Decimal:
		return self.product.price * self.quantity


class CartResponse(BaseModel):
	items: list[CartItemResponse]
	total: Decimal


