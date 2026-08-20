from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependency import get_db, require_admin
from app.models import User
from app.schemas.products import CategoryCreateRequest, CategoryResponse
from app.services import products as product_service

router = APIRouter()


@router.get('/categories', response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return product_service.list_categories(db)


@router.post('/categories', response_model=CategoryResponse)
def create_category(
    payload: CategoryCreateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return product_service.create_category(db, payload.name, payload.slug, payload.parent_id)