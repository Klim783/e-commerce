from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import WishlistItem
from app.models import Product


def get_wishlist_item(db: Session, user_id: int, product_id: int) -> WishlistItem | None:
    stmt = select(WishlistItem).where(
        WishlistItem.user_id == user_id, WishlistItem.product_id == product_id
    )
    return db.execute(stmt).scalar_one_or_none()


def get_wishlist(db: Session, user_id: int) -> list[WishlistItem]:
    stmt = select(WishlistItem).where(WishlistItem.user_id == user_id)
    return db.execute(stmt).scalars().all()


def add_item(db: Session, user_id: int, product_id: int) -> WishlistItem:
    item = WishlistItem(user_id=user_id, product_id=product_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def remove_item(db: Session, item: WishlistItem) -> None:
    db.delete(item)
    db.commit()