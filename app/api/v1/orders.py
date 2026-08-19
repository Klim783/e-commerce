from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.dependency import get_db, get_current_user
from app.schemas.order import OrderResponse
from app.services import orders as order_service
from app.dependency import require_admin
from app.schemas.order import AdminOrderResponse, OrderStatusUpdateRequest

router = APIRouter()

@router.post('/checkout', response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def checkout(db:Session = Depends(get_db), user = Depends(get_current_user)):
	return order_service.checkout(db, user.id)

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id:int,db:Session = Depends(get_db), user = Depends(get_current_user)):
	return order_service.get_order(db, user.id, order_id)

@router.post("/",response_model=list[OrderResponse])
def list_orders(db:Session = Depends(get_db), user = Depends(get_current_user)):
	return order_service.list_orders(db, user.id)

@router.get("/admin/all", response_model=list[AdminOrderResponse])
def admin_list_orders(
	order_status:str|None = None,
	db:Session = Depends(get_db),
	admin = Depends(require_admin),
):
	return order_service.admin_list_orders(db, order_status)

@router.patch("/admin/{order_id}/status",response_model=AdminOrderResponse)
def admin_update_status(
	order_id:int,
	payload:OrderStatusUpdateRequest,
	db:Session = Depends(get_db),
	admin = Depends(require_admin),
):
	return order_service.admin_update_order_status(db, order_id, payload.status.value)
