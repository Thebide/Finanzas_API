from fastapi import APIRouter

from .incomes_route import incomes_router
from .expenses_route import expenses_router

v1_router = APIRouter(
    prefix="/v1", 
    responses={ 400:{"Description": "Bad Request"},}
)

v1_router.include_router(incomes_router, tags=["Incomes"])
v1_router.include_router(expenses_router, tags=["Expenses"])
