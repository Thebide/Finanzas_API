from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from .base_model import BaseModel

class IncomeModel(BaseModel):
    __tablename__ = 'incomes'

    name: Mapped[str] = mapped_column(String(50) ,nullable=False)
    description: Mapped[str] = mapped_column(String(1000) ,nullable=False)
    quantity: Mapped[int] = mapped_column(Integer() ,nullable=False)
