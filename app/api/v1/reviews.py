from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.dependency import get_db, get_current_user
from app.schemas.review import CreateReviewRequest, UpdateReviewRequest, ReviewResponse
from app.services import reviews as review_service


router = APIRouter(prefix = "/reviews", tags = ["reviews"])

@router.post("/", response_model=ReviewResponse, status_code = status.HTTP_201_CREATED)
def create_review(
	payload:CreateReviewRequest,
	db:Session = Depends(get_db),
	user = Depends(get_current_user),
):
	return review_service.create_review(db, user.id, payload.product_id, payload.rating, payload.commet)

@router.post("/{review_id}", response_model=ReviewResponse)
def update_review(
	review_id:int,
	payload:UpdateReviewRequest,
	db:Session = Depends(get_db),
	user = Depends(get_current_user)
):
	return review_service.update_review(db, user.id, review_id, payload.rating, payload.comment)

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id:int, db:Session = Depends(get_db), user = Depends(get_current_user)):
	review_service.delete_review(db, user.id, review_id)


@router.get("/products/{product_id")
def list_reviews(product_id:int, db:Session = Depends(get_db)):
	reviews,summary = review_service.list_reviews(db, product_id)
	return {"reviews":reviews, "summary":summary}