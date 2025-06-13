from .base_repository import BaseRepository
from src.database.models import ExpenseModel

class ExpenseRepositiry(BaseRepository):
  def __init__(self):
    super().__init__(ExpenseModel)