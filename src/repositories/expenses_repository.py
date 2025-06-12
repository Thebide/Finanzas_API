from .base_repository import BaseRepository
from src.helpers.jsondb import read_json, write_json
from typing import List, Dict, Any
from src.config.settings import Settings
from .base_repository import BaseModel
from src.database.models import ExpenseModel

class ExpenseRepositiry(BaseRepository):
  def __init__(self):
    super().__init__(ExpenseModel)
  
  
  async def _read_all(self) -> List[Dict[str, Any]]:
    data = read_json(Settings.PATH_DATA)
    return data.get("expenses", []) 
  
  async def _update_db(self, db:List[Dict[str, Any]]) -> None:
    current = read_json(Settings.PATH_DATA)
    current["expenses"] = db
    write_json(Settings.PATH_DATA, current)
  
  async def _netx_id(self) -> int:
    data = await self._read_all()
    if not data:
        return 1
    return max(expense["id"] for expense in data) + 1