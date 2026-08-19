# from datetime import datetime, timezone
# from decimal import Decimal
# from sqlalchemy import ForeignKey, DateTime, UniqueConstraint
# from enum import Enum as PyEnum
# from app.models import Base, utcnow
# from IPython.core.completer import back_unicode_name_matcher
# from sqlalchemy import ForeignKey, String, Text, Numeric, Integer, Boolean, Enum as SQLEnum, func, UniqueConstraint
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from app.database import Base
#
#
# class UserRole(str, PyEnum):
# 	CUSTOMER = 'CUSTOMER'
# 	ADMIN = 'ADMIN'
#
# class OrderStatus(str, PyEnum):
# 	PENDING = 'PENDING'
# 	PAID = 'PAID'
# 	SHIPPED = 'SHIPPED'
# 	DELIVERED = 'DELIVERED'
# 	CANCELLED = 'CANCELLED'
#
# class PaymentStatus(str, PyEnum):
# 	PENDING = 'PENDING'
# 	SUCCEEDED = 'SUCCEEDED'
# 	FAILED = 'FAILED'
#
#
# #User
#
# class User(Base):
# 	__tablename__ = "user"
#
# 	id: Mapped[int] = mapped_column(primary_key=True)
# 	email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
# 	hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
# 	full_name: Mapped[str] = mapped_column(String(255), nullable=False)
# 	role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.CUSTOMER, nullable=False)
# 	created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), server_default=func.now())
#
# 	cart: Mapped["Cart"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
# 	orders: Mapped[list["Order"]] = relationship(back_populates="user")
# 	reviews: Mapped[list["Review"]] = relationship(back_populates="user")
#
#
# #Catalog
#
# class Category(Base):
# 	__tablename__ = 'category'
#
# 	id:Mapped[int] = mapped_column(primary_key=True)
# 	name:Mapped[str] = mapped_column(String(255), nullable=False)
# 	slug:Mapped[str] = mapped_column(String(255), unqiue = True, index = True, nullable = False)
# 	parent_id:Mapped[int|None] = mapped_column(ForeignKey('categoty.id'), nullable = False)
#
# 	parent:Mapped["Category"|None] = relationship(remote_side = 'Category.id', back_populates='children')
# 	children:Mapped[list['Category']] = relationship(back_populates='parent')
# 	products:Mapped[list["Product"]] = relationship(back_populates = 'category')
#
# class Product(Base):
# 	__tablename__ = 'product'
# 	id:Mapped[int] = mapped_column(primary_key=True)
# 	name:Mapped[str] = mapped_column(String(255), nullable=False)
# 	slug:Mapped[str] = mapped_column(String(255), unique = True, index = True, nullable=False)
# 	description:Mapped[str] = mapped_column(String(255), nullable=True)
# 	price:Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
# 	stock_quantity : Mapped[int] = mapped_column(Integer, default=0, nullable = False)
# 	image_url:Mapped[str|None] = mapped_column(String(500), nullable = False)
# 	is_active:Mapped[bool] = mapped_column(Boolean, default = True, nullable = False)
# 	created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), server_default=func.now())
#
# 	category_id:Mapped[int] = mapped_column(ForeignKey('category.id'), nullable = False)
# 	category:Mapped['Category'] = relationship(back_populates='products')
#
# 	cart_items: Mapped[list["CartItem"]] = relationship(back_populates="product")
# 	order_items: Mapped[list["OrderItem"]] = relationship(back_populates="product")
# 	reviews: Mapped[list["Review"]] = relationship(back_populates="product", cascade="all, delete-orphan")
#
#
# #Cart
#
# class Cart(Base):
# 	__tablename__ = 'cart'
# 	id:Mapped[int] = mapped_column(primary_key=True)
# 	user_id:Mapped[int] = mapped_column(ForeignKey('user.id'),unique=True, nullable=False)
#
# 	user: Mapped["User"] = relationship(back_populates="cart")
# 	items: Mapped[list["CartItem"]] = relationship(back_populates="cart", cascade="all, delete-orphan")
#
# class Cart(Base):
# 	__tablename__ = 'cart'
# 	id:Mapped[int] = mapped_column(primary_key=True)
# 	user_id:Mapped[int] = mapped_column(ForeignKey('user.id'),unique=True, nullable=False)
# 	items:Mapped[list["CartItem"]] = relationship(back_populates="cart", cascade = "all, delete-orphan")
#
#
#
# class CartItem(Base):
# 	__tablename__ = "cart_item"
# 	__table_args_ = (UniqueConstraint("cart_id", "product_id", name = 'uq_cart_product'),)
#
# 	id:Mapped[int] = mapped_column(primary_key=True)
# 	cart_id:Mapped[int] = mapped_column(ForeignKey('cart.id'), nullable=False)
# 	product_id:Mapped[int] = mapped_column(ForeignKey('product.id'), nullable = False)
# 	quantity:Mapped[int] = mapped_column((Integer), nullable = False, default = 1)
#
# 	cart: Mapped['Cart'] = relationship(back_populates='items')
# 	product:Mapped["Product"] = relationship(back_populates="cart_items")
#
#
# #Orders
# class Order(Base):
# 	__tablename__ = 'order'
#
# 	id:Mapped[int] = mapped_column(primary_key=True)
# 	user_id:Mapped[int] = mapped_column(ForeignKey('user.id'),unique=True, nullable=False)
# 	status:Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus), default = OrderStatus.PENDING, nullable = False)
# 	total_amount:Mapped[Decimal] = mapped_column(Numeric(10,2), nullable = False)
# 	shipping_address:Mapped[str] = mapped_column(String(500), nullable = False)
# 	created_at:Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), server_default=func.now())
#
# 	user:Mapped["User"] = relationship(back_populates="orders")
# 	items:Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade = "all, delete-orphan")
# 	payment:Mapped["Payment|None"] = relationship(back_populates="order", utelist = False, cascade = "all, delete-orphan")
#
#
# class OrderItem(Base):
# 	__tablename__ = 'order_item'
# 	id:Mapped[int] = mapped_column(primary_key=True)
# 	order_id:Mapped[int] = mapped_column(ForeignKey('order.id'), nullable = False)
# 	product_id:Mapped[int] = mapped_column(ForeignKey('product.id'), nullable = False)
# 	quantity:Mapped[int] = mapped_column(Integer, nullable = False)
#
# 	price_at_purchase:Mapped[Decimal] = mapped_column(Numeric(10,2), nullable = False)
# 	order:Mapped["Order"] = relationship(back_populates = "items")
# 	product:Mapped["Product"] = relationship(back_populates="order_items")
#
# class Payment(Base):
# 	__tablename__ = "payment"
#
# 	id:Mapped[int] = mapped_column(primary_key=True)
# 	order_id:Mapped[int] = mapped_column(ForeignKey("order.id"), unique = True, nullable = False)
# 	provider:Mapped[str] = mapped_column(String(50), default = "mock_stripe", nullable = False)
#
# 	status : Mapped[PaymentStatus] = mapped_column(SQLEnum(PaymentStatus),default=PaymentStatus.PENDING, nullable=False)
# 	amount:Mapped[Decimal]= mapped_column(Numeric(10,2), nullable = False)
# 	transaction_id:Mapped[str|None] = mapped_column(String(255), nullable = True)
# 	created_at :Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), server_default=func.now())
#
# 	order:Mapped["Order"] = relationship(back_populates = "payments")
#
#
# class Review(Base):
# 	__tablename__ = 'review'
# 	__table_args__ = (UniqueConstraint("product_id", "user_id", name="uq_review_product_user"),)
#
# 	id:Mapped[int] = mapped_column(primary_key=True)
# 	product_id:Mapped[int] = mapped_column(ForeignKey('product.id'), nullable = False)
# 	user_id = Mapped[int] = mapped_column(ForeignKey("user.id"), nullable = False)
# 	rating:Mapped[int] = mapped_column(Integer, nullable = False)
#
# 	comment:Mapped[str|None] = mapped_column(Text, nullable = True)
# 	created_at:Mapped[datetime] = mapped_column(default=lambda:datetime.now(timezone.utc), server_default=func.now())
#
# 	product:Mapped["Product"] = relationship(back_populates="reviews")
# 	user:Mapped["User"] = relationship(back_populates="reviews")
#
# class WishlistItem(Base):
#     __tablename__ = "wishlist_items"
#     __table_args__ = (UniqueConstraint("user_id", "product_id", name="uq_wishlist_user_product"),)
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
#     added_at: Mapped[object] = mapped_column(DateTime, default=utcnow)


from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum as PyEnum

from sqlalchemy import (
    ForeignKey, String, Text, Numeric, Integer, Boolean,
    Enum as SQLEnum, UniqueConstraint, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserRole(str, PyEnum):
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"


class OrderStatus(str, PyEnum):
    PENDING = "PENDING"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class PaymentStatus(str, PyEnum):
    PENDING = "PENDING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), server_default=func.now())

    cart: Mapped["Cart"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    orders: Mapped[list["Order"]] = relationship(back_populates="user")
    reviews: Mapped[list["Review"]] = relationship(back_populates="user")

class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("category.id"), nullable=True)

    parent: Mapped["Category | None"] = relationship(remote_side="Category.id", back_populates="children")
    children: Mapped[list["Category"]] = relationship(back_populates="parent")
    products: Mapped[list["Product"]] = relationship(back_populates="category")


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), server_default=func.now())

    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=False)
    category: Mapped["Category"] = relationship(back_populates="products")

    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="product")
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="product")
    reviews: Mapped[list["Review"]] = relationship(back_populates="product", cascade="all, delete-orphan")

class Cart(Base):
    __tablename__ = "cart"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True, nullable=False)

    user: Mapped["User"] = relationship(back_populates="cart")
    items: Mapped[list["CartItem"]] = relationship(back_populates="cart", cascade="all, delete-orphan")


class CartItem(Base):
    __tablename__ = "cart_item"
    __table_args__ = (UniqueConstraint("cart_id", "product_id", name="uq_cart_product"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("cart.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    cart: Mapped["Cart"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship(back_populates="cart_items")


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    shipping_address: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")
    payment: Mapped["Payment | None"] = relationship(back_populates="order", uselist=False, cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_at_purchase: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship(back_populates="order_items")


class Payment(Base):
    __tablename__ = "payment"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"), unique=True, nullable=False)
    provider: Mapped[str] = mapped_column(String(50), default="mock_stripe", nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    transaction_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), server_default=func.now())

    order: Mapped["Order"] = relationship(back_populates="payment")


class Review(Base):
    __tablename__ = "review"
    __table_args__ = (UniqueConstraint("product_id", "user_id", name="uq_review_product_user"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), server_default=func.now())

    product: Mapped["Product"] = relationship(back_populates="reviews")
    user: Mapped["User"] = relationship(back_populates="reviews")


class WishlistItem(Base):
    __tablename__ = "wishlist_item"
    __table_args__ = (UniqueConstraint("user_id", "product_id", name="uq_wishlist_user_product"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), nullable=False)
    added_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), server_default=func.now())