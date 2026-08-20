from fastapi import APIRouter, Depends
from igraph import palettes

from sqlalchemy.orm import Session
from app.dependency import get_db, get_current_user
from app.models import User
from app.schemas.users import RegisterRequest, LoginRequest, TokenResponse, UserResponse

from app.services import users as users_service

router = APIRouter()


@router.post('/auth/register', response_model=UserResponse)
def register(payload:RegisterRequest, db:Session = Depends(get_db)):
	return users_service.register(db, payload.email, payload.password, payload.full_name)

@router.post('/auth/login', response_model=TokenResponse)
def login(payload:LoginRequest, db:Session = Depends(get_db)):
	return users_service.login(db, payload.email, payload.password)

@router.get('/auth/me', response_model=UserResponse)
def get_me(current_user:User = Depends(get_current_user)):
	return UserResponse.model_validate(current_user)