from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, Integer
from .base_model import BaseModel

class ExpenseModel(BaseModel):
    __tablename__ = "expenses"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer(), nullable=False)
    fees: Mapped[int] = mapped_column(Integer(), nullable=False)
    payment_date: Mapped[date] = mapped_column(Date(), nullable=False)
    estimated_next_payment_date : Mapped[date] = mapped_column(Date(), nullable=False)
