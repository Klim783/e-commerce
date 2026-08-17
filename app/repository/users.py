from sqlalchemy.orm import Session
from app.models import User,Cart

def get_user_by_email(db:Session, email:str) -> User|None:
	return db.query(User).filter(User.email == email).first()

def get_user_by_id(db:Session, user_id:int) ->User|None:
	return db.query(User).filter(User.id == user_id).first()


def create_user(db:Session, email:str, hashed_password:str, full_name:str) -> User:
	user = User(email = email, hashed_password = hashed_password, full_name = full_name)
	db.add(user)
	db.flush()

	cart = Cart(user_id = user.id)
	db.add(cart)
	db.refresh(user)
	return user