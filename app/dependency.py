from typing import Generator

from fastapi import Depends, HTTPException

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User, UserRole
from app.repository import users as users_repository
from app.security import decode_access_token

security = HTTPBearer()

def get_db() -> Generator[Session,None,None]:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

def get_current_user(
		credentials: HTTPAuthorizationCredentials = Depends(security),
		db:Session = Depends(get_db),
) -> User:
	email = decode_access_token(credentials.credentials)
	if not email:
		raise HTTPException(status_code = 401, detail="Invalid or expired token")
	user = users_repository.get_user_by_email(db, email)
	if not user:
		raise HTTPException(status_code = 401, detail = 'User not found')
	return user


