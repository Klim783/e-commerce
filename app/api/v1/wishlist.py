from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.dependency import get_db, get_current_user
from app.schemas.wishlist import AddToWishlistRequest, WishlistItemResponse
from app.services import wishlist as wishlist_service

router = APIRouter(prefix="/wishlist", tags=["wishlist"])


@router.get("/", response_model=list[WishlistItemResponse])
def view_wishlist(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return wishlist_service.list_wishlist(db, user.id)


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_item(
    payload: AddToWishlistRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return wishlist_service.add_to_wishlist(db, user.id, payload.product_id)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item(product_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    wishlist_service.remove_from_wishlist(db, user.id, product_id)