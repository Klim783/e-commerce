from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repository import reviews as review_repo

def create_review(db:Session, user_id:int, product_id:int, rating:int, comment:str|None):
	if not review_repo.has_purchased(db, user_id, product_id):
		raise HTTPException(
			status.HTTP_403_FORBIDDEN,
			"You can only review products you've purchased",
		)
	if review_repo.get_review_by_user_and_product(db, user_id, product_id):
		raise HTTPException(status.HTTP_400_BAD_REQUEST, 'You have already reviewed this product')
	return review_repo.create_review(db, user_id, product_id, rating, comment)

def update_review(db:Session, user_id:int, review_id:int, rating:int, comment:str|None):
	review = review_repo.get_review_by_id(db, review_id)
	if review is None:
		raise HTTPException(status.HTTP_404_NOT_FOUND, 'Review not found')
	if review.user_id != user_id:
		raise HTTPException(status.HTTP_403_FORBIDDEN, 'Not your review')
	return review_repo.update_review(db, review, rating, comment)


def delete_review(db:Session, user_id:int, review_id:int):
	review = review_repo.get_review_by_id(db, review_id)
	if review is None:
		raise HTTPException(status.HTTP_404_NOT_FOUND, 'Review not found')
	if review.user_id != user_id:
		raise HTTPException(status.HTTP_403_FORBIDDEN, 'Not your review')
	review_repo.delete_review(db, review)

def list_reviews(db:Session, product_id:int):
	reviews = review_repo.get_reviews_for_product(db, product_id)
	avg,count = review_repo.get_rating_summary(db, product_id)
	return reviews, {"average_rating":avg, "review_count":count}
