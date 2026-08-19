from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repository import wishlist as wishlist_repo
from app.repository import cart as cart_repo  # reuse get_product


def add_to_wishlist(db: Session, user_id: int, product_id: int):
    if cart_repo.get_product(db, product_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")
    if wishlist_repo.get_wishlist_item(db, user_id, product_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Already in wishlist")
    return wishlist_repo.add_item(db, user_id, product_id)


def remove_from_wishlist(db: Session, user_id: int, product_id: int):
    item = wishlist_repo.get_wishlist_item(db, user_id, product_id)
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not in wishlist")
    wishlist_repo.remove_item(db, item)


def list_wishlist(db: Session, user_id: int):
    return wishlist_repo.get_wishlist(db, user_id)