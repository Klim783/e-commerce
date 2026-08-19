from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependency import get_db, get_current_user
from app.schemas.cart import AddToCartRequest, UpdateCartItemRequest, CartResponse
from app.services import cart as cart_service

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/", response_model=CartResponse)
def view_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return cart_service.get_cart(db, user.id)


@router.post("/items", status_code=status.HTTP_201_CREATED)
def add_item(
    payload: AddToCartRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return cart_service.add_to_cart(db, user.id, payload.product_id, payload.quantity)


@router.put("/items/{product_id}")
def update_item(
    product_id: int,
    payload: UpdateCartItemRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return cart_service.update_cart_item(db, user.id, product_id, payload.quantity)


@router.delete("/items/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    cart_service.remove_from_cart(db, user.id, product_id)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
    cart_service.clear_cart(db, user.id)