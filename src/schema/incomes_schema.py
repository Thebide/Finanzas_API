from typing import Optional,Annotated,List
from datetime import datetime

from pydantic import BaseModel, Field
from .pagination_schema import Pagination

class newincomes_recuest(BaseModel):
    name: str
    description: str = Field(..., min_length=2, max_length=100)
    quantity: float = Field(ge=1) #superior a 1
     

class update_incomes_recuest(BaseModel):
    name: Optional[str]
    description: Optional[str] = Field(..., min_length=2, max_length=100)
    quantity: Optional[float] = Field(ge=1) #superior a 1


class incomes_response(BaseModel):
    id: int
    name: str
    desciption: str
    quantity: float #superior 1
    created: datetime
    Update: datetime

class incomes_pagination(BaseModel):
    result: List[incomes_response]
    meta: Pagination