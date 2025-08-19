from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import create_session
from schemas import OrderSchema
from models import Order


order_router = APIRouter(prefix="/orders", tags=["orders"])


@order_router.get("/")
async def orders():
    """
    Default orders route
    """
    return {"message": "List of orders"}


@order_router.post("/create")
async def create_order(
    order_schema: OrderSchema, session: Session = Depends(create_session)
):
    new_order = Order(user_id=order_schema.user_id)

    session.add(new_order)
    session.commit()
    return {"message": f"pedido criado com sucesso! ID do pedido {new_order.id}"}
