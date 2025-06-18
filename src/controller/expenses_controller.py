import logging

from src.schema.expenses_schema import NewExpensesRecuest, UpdateExpensesRecuest, ExpensesPagination, ExpensesResponse
from src.exceptions.server_exception import InternalServerError
from src.services.expenses_service import ExpensesService
from src.exceptions.client_exception import NotFound
from src.exceptions.base_HTTP_exception import BaseHTTPExceptions

logger = logging.getLogger(__name__)

class expensescontroller():
    def __init__(self, expenses_service: ExpensesService):
        self.expenses_service = expenses_service


    async def get_paginated (self, offset: int, limit: int) -> ExpensesPagination:
        try:
            return await self.expenses_service.get_paginated(offset, limit)
        except BaseHTTPExceptions as ex:
            raise ex
        except NotFound as ex:
            logger.error(f"Error en la paginación de gastos.")
            raise NotFound(message="EXPENSE_PAGE_NOT_FOUND")
        except Exception as ex:
            logger.critical(f"Error no contemplado en get_paginated_expenses. {ex}")
            raise InternalServerError(
                message=f"Error al listar gastos",
                exception_code='EXPENSE_UNHANDLED_ERROR'
            )

    async def create (self, data: NewExpensesRecuest) -> ExpensesResponse:
        try:
            return await self.expenses_service.create(data)
        except Exception as ex:
            logger.critical("Error no contemplado en create_expenses")
            raise InternalServerError(
            message=f"Error de creación de gasto {data.name}: {str(ex)}",
            exception_code='EXPENSE_UNHANDLED_ERROR'
            )
        

    async def search (self, expense_id: int) -> ExpensesResponse:
        try:
            return await self.expenses_service.search(expense_id)
        except NotFound as ex:
            logger.error(f"Error en la busqueda del gasto #{expense_id}. {ex}")
            raise NotFound(message="EXPENSE_NOT_FOUND")
        except Exception as ex:
            logger.critical(f"Error no contemplado en search_expenses. {ex}")
            raise InternalServerError(
            message=f"Error de busqueda del gasto N°{expense_id}. {ex}",
            exception_code='EXPENSE_UNHANDLED_ERROR'
            )

    async def update (self, expense_id: int, data: UpdateExpensesRecuest) -> ExpensesResponse:
        try:
            return await self.expenses_service.update(expense_id , data)
        except NotFound as ex:
            logger.error(f"Error en la actualización del gasto #{expense_id}. {ex}")
            raise NotFound(message="EXPENSE_NOT_FOUND")
        except Exception as ex:
            logger.critical(f"Error no contemplado en update_expenses. {ex}")
            raise InternalServerError(
            message=(f"Error de actualización del gasto N°{expense_id}, {data.name}: {str(ex)}"),
            exception_code='EXPENSE_UNHANDLED_ERROR'
            )

    async def delete (self, expense_id: int) -> None:
        try:
            return await self.expenses_service.delete(expense_id)
        except NotFound as ex:
            logger.error(f"Error de eliminación del gasto N°{expense_id}.")
            raise NotFound(message="EXPENSE_NOT_FOUND")
        except Exception as ex:
            logger.critical("Error no contemplado en delete_expenses")
            raise InternalServerError(
            message=f"Error de eliminación del gasto N°{expense_id}",
            exception_code='EXPENSE_UNHANDLED_ERROR'
            )
