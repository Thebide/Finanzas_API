import asyncio
import logging
from typing import List

from src.schema.incomes_schema import newincomes_recuest, update_incomes_recuest, incomes_response, incomes_pagination
from src.exceptions.app_exception import NotFoundError
from src.repositories.incomes_repository import IncomesRepository

logger = logging.getLogger(__name__)

class IncomesService():
    def __init__(self, incomes_repository: IncomesRepository = IncomesRepository()):
        self.incomes_repository = incomes_repository

    async def get_paginated (self, offset: int, limit: int) -> incomes_pagination:
        logger.debug(f"Obteniendo lista de ingresos paginados. Pagina:{offset} , Limite:{limit}")
        total_item, incomes = await asyncio.gather(
            self.__couting(),
            self.__get_incomes_list(offset, limit),
            )
        total_page = (total_item // limit) + (0 if total_item % limit == 0 else 1)
        total_page = 1 if (offset == 1 and total_item == 0) else (total_page)
        if offset > total_page:
            raise NotFoundError
        logger.debug(f"Gastos obtenidos:{len(incomes)}")
        return incomes_pagination (
            result=incomes,
            meta={
                "concurrent_page": offset,
                "items_per_page": limit,
                "total_pages": total_page,
                "total_items": total_item,
            }
        )
    
    async def create (self, data: newincomes_recuest) -> incomes_response:
        logger.debug(f"Creando ingreso: {data}")
        new_incomes = await self.incomes_repository.create(data.model_dump(mode="json"))
        logger.debug(f"Gasto creado:{new_incomes}")
        return incomes_response.model_validate(new_incomes)

    async def search (self, income_id: int) -> incomes_response:
        logger.debug(f"Buscando ingreso:{income_id}")
        income = await self.incomes_repository.search_by({"id":income_id})
        if income is None:
            raise NotFoundError(f"El ingreso #{income_id} no existe")
        return incomes_response.model_validate(income)
        

    async def update (self, income_id: int, data: update_incomes_recuest) -> incomes_response:
        logger.debug(f"Actualizando ingreso:{income_id}")
        income = await self.incomes_repository.update_one({"id":income_id}, data.model_dump(mode="json", exclude_unset=True))
        if income is None:
            raise NotFoundError(f"El ingreso #{income_id} no existe")
        return incomes_response.model_validate(income)
        

    async def delete (self, income_id: int) -> None:
        logger.debug(f"Borrando ingreso:{income_id}")
        deleted = await self.incomes_repository.delete_one({"id":income_id})
        if not deleted:
            raise NotFoundError(f"El gasto #{income_id} no existe")
        return None
        

    async def __couting(self) -> int:
        return await self.incomes_repository.count()
    
    async def __get_incomes_list(self, offset: int, limit: int) -> List[incomes_response]:
        return await self.incomes_repository.get_list(offset, limit) 