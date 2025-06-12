from typing import Optional,Annotated,List
from datetime import date,datetime

from pydantic import BaseModel, Field
from .pagination_schema import Pagination

class NewExpensesRecuest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=2, max_length=100)
    quantity: float = Field(ge=1) #superior a 1
    fees : Optional[int] = 0  #cuotas
    payment_date: date 
    estimated_next_payment_date: Optional[date] = "1999-01-01" 

class UpdateExpensesRecuest(BaseModel):
    name: Optional[str]
    description: Optional[str] = Field(..., min_length=2, max_length=100)
    quantity: Optional[float] = Field(ge=1) #superior a 1
    fees : Optional[int] = 0  #cuotas
    payment_date: Optional[date] 
    estimated_next_payment_date: Optional[date] = "" 

class ExpensesResponse(BaseModel):
    id: int
    name: str
    description: str
    quantity: float #superior 1
    fees: int #cuotas
    payment_date: date
    estimated_next_payment_date : Optional[date]
    create: datetime
    update: datetime

class ExpensesPagination(BaseModel):
    result: List[ExpensesResponse]
    meta: Pagination