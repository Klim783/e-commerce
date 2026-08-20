from datetime import datetime
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class CategoryCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    slug: str = Field(..., min_length=1, max_length=150)
    parent_id: int | None = None


class CategoryResponse(BaseModel):
    model_config = {'from_attributes': True}
    id: int
    name: str
    slug: str
    parent_id: int | None


class ProductCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    price: Decimal
    stock_quantity: int = Field(..., ge=0)
    category_id: int

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("Price must be positive")
        return v


class ProductUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    price: Decimal | None = None
    stock_quantity: int | None = Field(default=None, ge=0)
    image_url: str | None = None
    is_active: bool | None = None

    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls, v: Decimal | None) -> Decimal | None:
        if v is not None and v <= 0:
            raise ValueError("Price must be positive")
        return v


class ProductResponse(BaseModel):
    model_config = {'from_attributes': True}
    id: int
    name: str
    slug: str
    description: str | None
    price: Decimal
    stock_quantity: int
    image_url: str | None
    is_active: bool
    category_id: int
    created_at: datetime


class ProductSortBy(str, Enum):
    price_asc = "price_asc"
    price_desc = "price_desc"
    newest = "newest"
    rating = "rating"


class ProductFilterParams(BaseModel):
    q: str | None = None
    category_id: int | None = None
    min_price: Decimal | None = None
    max_price: Decimal | None = None
    min_rating: float | None = None
    sort_by: ProductSortBy = ProductSortBy.newest
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class PaginatedProductsResponse(BaseModel):
    items: list[ProductResponse]
    total: int
    page: int
    page_size: int
    total_pages: int