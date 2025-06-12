from typing import Optional, Dict, List, Any
from abc import ABC, abstractmethod
from datetime import datetime

class BaseRepository(ABC):
    
    async def count(self, criteria: Optional[dict] = {}) -> int:
        data = await self._read_all() 
        if criteria:
            data = [item for item in data if all(item.get(key) == value for key,value in criteria.items())]
        return len(data)
    
    async def get_list(self, offset: int, limit: int, criteria: Optional[dict] = {}) -> list[dict]:
        data = await self._read_all()
        if criteria:    
            data = [item for item in data if all(item.get(key) == value for key,value in criteria.items())]
        start = (offset - 1) * limit
        end = start + limit
        return data[start:end]
    
    async def create(self, data: dict) -> dict:
        data["id"] = await self._netx_id()
        data["create"] = datetime.now().isoformat()
        data["update"] = datetime.now().isoformat()
        db = await self._read_all()
        db.append(data)
        await self._update_db(db)
        return data

    async def search_by(self, criteria: dict) -> dict | None:
        data = await self._read_all()
        for item in data:
            if all(item.get(key) == value for key, value in criteria.items()):
                return item
        return None

    async def update_one(self, data: dict, criteria: dict) -> dict | None:
        db = await self._read_all()
        for index, item in enumerate(db):
            if all(item.get(key) == value for key, value in criteria.items()):
                item.update(data)
                item['update'] = datetime.now().isoformat()
                await self._update_db(db)
                return item
        return None

    async def update_many(self, data: dict, criteria: dict) -> dict | None:
        pass

    async def delete_one(self, criteria: dict) -> None:
        data = await self._read_all()
        for index, item in enumerate(data):
            if all(item.get(key) == value for key, value in criteria.items()):
                del data[index]
                await self._update_db(data)
                return True
        return False

    async def delete_many(self, criteria: dict) -> None:
        pass

    async def _update_all(self, db:List[Dict[str, Any]]) -> None:
        pass

    @abstractmethod
    async def _read_all(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def _update_db(self, db:List[Dict[str, Any]]) -> None:
        pass

    @abstractmethod
    async def _netx_id(self) -> int:
        pass