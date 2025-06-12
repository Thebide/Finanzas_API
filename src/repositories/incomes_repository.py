from .base_repository import BaseRepository
from src.helpers.jsondb import read_json, write_json
from typing import List, Dict, Any
from src.config.settings import Settings
from .base_repository import BaseModel
from src.database.models import IncomeModel

class IncomesRepository(BaseRepository):
  def __init__(self):
    super().__init__(IncomeModel)


  async def _read_all(self) -> List[Dict[str, Any]]:
    data = read_json(Settings.PATH_DATA)
    return data.get("incomes", []) 
  
  async def _update_db(self, db:List[Dict[str, Any]]) -> None:
    current = read_json(Settings.PATH_DATA)
    current["incomes"] = db
    write_json(Settings.PATH_DATA, current)
  
  async def _netx_id(self) -> int:
    data = await self._read_all()
    if not data:
        return 1
    return max(income["id"] for income in data) + 1