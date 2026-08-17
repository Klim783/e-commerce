from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repository import users as users_repository
from app.schemas.users import UserResponse, TokenResponse

from app.security import hash_password, verify_password, create_access_token


def register(db:Session, email:str, password:str, full_name:str) -> UserResponse:
	if users_repository.get_user_by_email(db, email):
		raise HTTPException(status_code = 400, detail="Email already registered")
	user = users_repository.create_user(db, email, hash_password(password), full_name)
	return UserResponse.model_validate(user)

def login(db :Session, email:str, password:str)->TokenResponse:
	user = users_repository.get_user_by_email(db, email)
	if not user or not verify_password(password, user.hashed_password):
		raise HTTPException(status_code = 400, detail = 'Invalid email or password')
	token = create_access_token(user.email)
	return TokenResponse.model_validate(token)

