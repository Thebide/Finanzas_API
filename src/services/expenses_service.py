import asyncio
import logging
from typing import List

from src.schema.expenses_schema import NewExpensesRecuest, ExpensesResponse, ExpensesPagination, UpdateExpensesRecuest
from src.exceptions.app_exception import NotFoundError
from src.repositories.expenses_repository import ExpenseRepositiry

logger = logging.getLogger(__name__)

class ExpensesService():
    def __init__(self, expense_repository: ExpenseRepositiry = ExpenseRepositiry()):
        self.expense_repository = expense_repository

    async def get_paginated (self, offset: int, limit: int) -> ExpensesPagination:
        logger.debug(f"Obteniendo lista de gastos paginados. Pagina:{offset} , Limite:{limit}")
        total_item, expenses = await asyncio.gather(
            self.__couting(),
            self.__get_expenses_list(offset, limit),
            )
        total_page = (total_item // limit) + (0 if total_item % limit == 0 else 1)
        total_page = 1 if (offset == 1 and total_item == 0) else (total_page)
        if offset > total_page:
            raise NotFoundError
        logger.debug(f"Gastos obtenidos:{len(expenses)}")
        return ExpensesPagination (
            result=expenses,
            meta={
                "concurrent_page": offset,
                "items_per_page": limit,
                "total_page": total_page,
                "total_items": total_item,
            }
        )
    
    async def create (self, data: NewExpensesRecuest) -> ExpensesResponse:
        logger.debug(f"Creando gasto: {data}")
        new_expense = await self.expense_repository.create(data.model_dump(mode="json"))
        logger.debug(f"Gasto creado:{new_expense}")
        return ExpensesResponse.model_validate(new_expense)

    async def search (self, expense_id: int) -> ExpensesResponse:
        logger.debug(f"Buscando gasto:{expense_id}")
        expense = await self.expense_repository.search_by({"id":expense_id})
        if expense is None:
            raise NotFoundError(f"El gasto #{expense_id} no existe")
        return ExpensesResponse.model_validate(expense)
    
    async def update (self, expense_id: int, data: UpdateExpensesRecuest) -> ExpensesResponse:
        logger.debug(f"Actualizando gasto:{expense_id}")
        expense = await self.expense_repository.update_one({"id":expense_id}, data.model_dump(mode="json", exclude_unset=True))
        if expense is None:
            raise NotFoundError(f"El gasto #{expense_id} no existe")
        return ExpensesResponse.model_validate(expense)

    async def delete (self, expense_id: int) -> None:
        logger.debug(f"Eliminando gato:{expense_id}")
        deleted = await self.expense_repository.delete_one({"id":expense_id})
        if not deleted:
            raise NotFoundError(f"El gasto #{expense_id} no existe")
        return None

    async def __couting(self) -> int:
        return await self.expense_repository.count()
    
    async def __get_expenses_list(self, offset: int, limit: int) -> List[ExpensesResponse]:
        return await self.expense_repository.get_list(offset, limit) 