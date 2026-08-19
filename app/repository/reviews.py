from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models import Review
from app.models import Order, OrderItem

def has_purchased(db:Session, user_id:int, product_id:int) -> bool:
	stmt = (
		select(OrderItem.id)
		.join(Order, Order.id == OrderItem.order_id)
		.where(
			Order.user_id == user_id,
			OrderItem.product_id == product_id,
			Order.status.in_(['PAID', 'SHIPPED'])
		)
		.limit(1)
	)
	return db.execute(stmt).first() is not None

def get_review_by_user_and_product(db:Session, user_id:int, product_id:int) -> Review|None:
	stmt = select(Review).where(Review.user_id == user_id, Review.product_id == product_id)
	return db.execute(stmt).scalar_one_or_none()

def get_review_by_id(db: Session, review_id: int) -> Review | None:
    return db.get(Review, review_id)


def get_reviews_for_product(db: Session, product_id: int) -> list[Review]:
    stmt = select(Review).where(Review.product_id == product_id).order_by(Review.created_at.desc())
    return db.execute(stmt).scalars().all()

def create_review(db:Session, user_id:int, product_id:int, rating:int, comment:str|None) -> Review:
	review = Review(user_id = user_id, product_id  = product_id, rating = rating, comment = comment)
	db.add(review)
	db.commit()
	db.refresh(review)
	return review


def update_review(db:Session, review:Review, rating:int, comment:str|None) -> Review:
	review.rating = rating
	review.comment = comment
	db.commit()
	db.refresh(review)
	return review

def delete_review(db:Session, review: Review) -> None:
	db.delete(review)
	db.commit()

def get_rating_summary(db: Session, product_id: int) -> tuple[float, int]:
    stmt = select(func.avg(Review.rating), func.count(Review.id)).where(Review.product_id == product_id)
    avg, count = db.execute(stmt).one()
    return (round(avg, 2) if avg else 0.0, count)