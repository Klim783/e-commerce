from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from app.models import UserRole

class RegisterRequest(BaseModel):
	email:EmailStr
	password:str = Field(..., min_length=6, max_length=127)
	full_name:str = Field(..., min_length=1, max_length=255)

class LoginRequest(BaseModel):
	email:EmailStr
	password:str

class TokenResponse(BaseModel):
	access_token:str
	token_type:str = 'bearer'

class UserResponse(BaseModel):
	model_config = {'from_attributes' : True}
	id:int
	email:EmailStr
	full_name:str
	role:UserRole
	created_at:datetime

