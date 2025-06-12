from typing import Optional, Dict, List, Any
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Type

from src.database import database_connection
from src.database.models import BaseModel

class BaseRepository(ABC):
    def __init__(self, Model:Type[BaseModel] ):
        self.db = database_connection.Session
        self.Model = Model

    async def count(self, criteria: dict = {}) -> int:
        # data = await self._read_all() 
        # if criteria:
        #     data = [item for item in data if all(item.get(key) == value for key,value in criteria.items())]
        # return len(data)
        count = self.db.query(self.Model).filter_by(**criteria).count()
        return count

    async def get_list(self, offset: int, limit: int, criteria: dict = {}) -> list[dict]:
        # data = await self._read_all()
        # if criteria:    
        #     data = [item for item in data if all(item.get(key) == value for key,value in criteria.items())]
        # start = (offset - 1) * limit
        # end = start + limit
        # return data[start:end]
        offset = (offset - 1) * limit
        records = self.db.query(self.Model).order_by("id").filter_by(**criteria).limit(limit).offset(offset).all
        return [self._to_dict(record) for record in records]
    
    async def create(self, data: dict) -> dict:
        # data["id"] = await self._netx_id()
        # data["create"] = datetime.now().isoformat()
        # data["update"] = datetime.now().isoformat()
        # db = await self._read_all()
        # db.append(data)
        # await self._update_db(db)
        # return data
        new_record =self.Model(**data)
        self.db.add(new_record)
        self.db.commit()
        self.db.refresh(new_record)
        return self._to_dict(new_record)

    async def search_by(self, criteria: dict) -> dict | None:
        # data = await self._read_all()
        # for item in data:
        #     if all(item.get(key) == value for key, value in criteria.items()):
        #         return item
        # return None
        record = self.db.query(self.Model).filter_by(**criteria).first()
        if record is None:
            return None
        return self._to_dict(record)

    async def update_one(self, data: dict, criteria: dict) -> dict | None:
        # db = await self._read_all()
        # for index, item in enumerate(db):
        #     if all(item.get(key) == value for key, value in criteria.items()):
        #         item.update(data)
        #         item['update'] = datetime.now().isoformat()
        #         await self._update_db(db)
        #         return item
        # return None
        record = self.db.query(self.Model).filter_by(**criteria).first()
        if record is None:
            return None
        for field, value in data.values():
            setattr(record, field, value)
        self.db.commit()
        self.db.refresh(record)
        return self._to_dict(record)

    async def update_many(self, data: dict, criteria: dict) -> dict | None:
        pass

    async def delete_one(self, criteria: dict) -> None:
        #data = await self._read_all()
        #for index, item in enumerate(data):
        #    if all(item.get(key) == value for key, value in criteria.items()):
        #        del data[index]
        #        await self._update_db(data)
        #        return True
        #return False
        record = self.db.query(self.Model).filter_by(**criteria).first()
        if record is None:
            return False
        self.db.delete(record)
        self.db.commit()
        return True
        

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

    def _to_dict(self, record: BaseModel) -> dict:
        return{
            column.name : getattr(record, column.name)
            for column in self.Model.__table__.columns
        }