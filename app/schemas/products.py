from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

class CategoryCreateRequest(BaseModel):
	name: str = Field(..., min_length=1, max_length=150)
	slug :str = Field(..., min_length=1, max_length=150)
	parent_id: int|None = None


class CategoryResponse(BaseModel):
	model_config = {'from_attributes':True}
	id:int
	name:str
	slug:str
	parent_id:int

class ProductCreateRequest(BaseModel):
	name:str = Field(..., min_length=1, max_length=255)
	slug:str = Field(..., min_length=1, max_length=255)
	description:str|None = None
	price:Decimal
	stock_quantity:int = Field(..., min_length=1, max_length=255)
	category_id:int

	@field_validator("price")
	def price_must_be_positive(cls, v:Decimal) -> Decimal:
		if v <= 0:
			raise ValueError("Price must be positive")
		return v


class ProductUpdateResponse(BaseModel):
	name: str|None = Field(..., min_length=1, max_length=255)
	description:str|None = None
	price:Decimal |None = None
	stock_quantity:int |None = Field(default=None, gt =0)
	image_url:str|None = None
	is_active: bool |None = None

	@field_validator('price')
	@classmethod
	def price_must_be_positive(cls, v :Decimal |None) -> Decimal:
		if v <= 0:
			raise ValueError("Price must be positive")
		return v


class ProductResponse(BaseModel):
	id:int
	name:str
	slug:str
	description:str
	price:Decimal
	stock_quantity:int
	image_url:str
	is_active:bool
	category_id:int
	created_at:datetime
