from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Cart, CartItem, Product


def get_cart_by_user(db: Session, user_id: int) -> Cart | None:
    stmt = select(Cart).where(Cart.user_id == user_id)
    return db.execute(stmt).scalar_one_or_none()


def create_cart(db: Session, user_id: int) -> Cart:
    cart = Cart(user_id=user_id)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


def get_or_create_cart(db: Session, user_id: int) -> Cart:
    cart = get_cart_by_user(db, user_id)
    if cart is None:
        cart = create_cart(db, user_id)
    return cart


def get_product(db: Session, product_id: int) -> Product | None:
    return db.get(Product, product_id)


def get_cart_item(db: Session, cart_id: int, product_id: int) -> CartItem | None:
    stmt = select(CartItem).where(
        CartItem.cart_id == cart_id,
        CartItem.product_id == product_id,
    )
    return db.execute(stmt).scalar_one_or_none()


def get_cart_items(db: Session, cart_id: int) -> list[CartItem]:
    stmt = select(CartItem).where(CartItem.cart_id == cart_id)
    return db.execute(stmt).scalars().all()


def create_cart_item(db: Session, cart_id: int, product_id: int, quantity: int) -> CartItem:
    item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_cart_item_quantity(db: Session, item: CartItem, quantity: int) -> CartItem:
    item.quantity = quantity
    db.commit()
    db.refresh(item)
    return item


def delete_cart_item(db: Session, item: CartItem) -> None:
    db.delete(item)
    db.commit()


def clear_cart(db: Session, cart_id: int) -> None:
    items = get_cart_items(db, cart_id)
    for item in items:
        db.delete(item)
    db.commit()