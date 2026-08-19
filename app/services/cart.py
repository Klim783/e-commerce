from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repository import cart as cart_repo


def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int):
    product = cart_repo.get_product(db, product_id)
    if product is None or not product.is_active:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")

    cart = cart_repo.get_or_create_cart(db, user_id)
    existing = cart_repo.get_cart_item(db, cart.id, product_id)
    requested_total = quantity + (existing.quantity if existing else 0)

    if requested_total > product.stock_quantity:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Only {product.stock_quantity} units available in stock",
        )

    if existing:
        return cart_repo.update_cart_item_quantity(db, existing, requested_total)
    return cart_repo.create_cart_item(db, cart.id, product_id, quantity)


def update_cart_item(db: Session, user_id: int, product_id: int, quantity: int):
    cart = cart_repo.get_or_create_cart(db, user_id)
    item = cart_repo.get_cart_item(db, cart.id, product_id)
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not in cart")

    product = cart_repo.get_product(db, product_id)
    if quantity > product.stock_quantity:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Only {product.stock_quantity} units available in stock",
        )

    return cart_repo.update_cart_item_quantity(db, item, quantity)


def remove_from_cart(db: Session, user_id: int, product_id: int):
    cart = cart_repo.get_or_create_cart(db, user_id)
    item = cart_repo.get_cart_item(db, cart.id, product_id)
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not in cart")
    cart_repo.delete_cart_item(db, item)


def clear_cart(db: Session, user_id: int):
    cart = cart_repo.get_or_create_cart(db, user_id)
    cart_repo.clear_cart(db, cart.id)


def get_cart(db: Session, user_id: int):
    cart = cart_repo.get_or_create_cart(db, user_id)
    items = cart_repo.get_cart_items(db, cart.id)

    result = []
    total = 0
    for item in items:
        product = cart_repo.get_product(db, item.product_id)
        subtotal = product.price * item.quantity
        total += subtotal
        result.append({
            "id": item.id,
            "product_id": product.id,
            "product_name": product.name,
            "unit_price": product.price,
            "quantity": item.quantity,
            "subtotal": subtotal,
        })

    return {"id": cart.id, "items": result, "total": total}