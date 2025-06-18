import logging

from src.schema.incomes_schema import newincomes_recuest, update_incomes_recuest, incomes_response, incomes_pagination
from src.exceptions.server_exception import InternalServerError
from src.services.incomes_service import IncomesService
from src.exceptions.client_exception import NotFound
from src.exceptions.base_HTTP_exception import BaseHTTPExceptions

logger = logging.getLogger(__name__)

class incomescontroller():
    def __init__(self, incomes_service: IncomesService):
        self.incomes_service = incomes_service


    async def get_paginated (self, offset: int, limit: int) -> incomes_pagination:
        try:
            return await self.incomes_service.get_paginated(offset, limit)
        except BaseHTTPExceptions as ex:
            raise ex
        except NotFound as ex:
            logger.error(f"Error en la paginación de ingresos.")
            raise NotFound(message="INCOME_PAGE_NOT_FOUND")
        except Exception as ex:
            logger.critical("Error no contemplado en get_paginated_incomes.")
            raise InternalServerError(
            message=f"Error al listar ingresos",
            exception_code='INCOME_UNHANDLED_ERROR'
            )

    async def create (self, data: newincomes_recuest) -> incomes_response:
        try:
            return await self.incomes_service.create(data)
        except Exception as ex:
            raise InternalServerError(
            message=f"Error de creación del ingreso {data.name}: {str(ex)}",
            exception_code='INCOME_UNHANDLED_ERROR'
            )
        

    async def search (self, income_id: int) -> incomes_response:
        try:
            return await self.incomes_service.search(income_id)
        except NotFound as ex:
            logger.error(f"Error en la busqueda del ingreso #{income_id}. {ex}")
            raise NotFound(message="INCOME_NOT_FOUND")
        except Exception as ex:
            raise InternalServerError(
            message=f"Error de busqueda del ingreso N°{income_id}. {ex}",
            exception_code='INCOME_UNHANDLED_ERROR'
            )

    async def update (self, income_id: int, data: update_incomes_recuest) -> incomes_response:
        try:
            return await self.incomes_service.update(income_id , data)
        except NotFound as ex:
            logger.error(f"Error en la busqueda del ingreso #{income_id}. {ex}")
            raise NotFound(message="INCOME_NOT_FOUND")
        except Exception as ex:
            raise InternalServerError(
            message=f"Error de actualización del ingreso N°{income_id}, {data.name}: {str(ex)}",
            exception_code='INCOME_UNHANDLED_ERROR'
            )

    async def delete (self, income_id: int) -> None:
        try:
            return await self.incomes_service.delete(income_id)
        except NotFound as ex:
            logger.error(f"Error en la busqueda del ingreso #{income_id}. {ex}")
            raise NotFound(message="INCOME_NOT_FOUND")
        except Exception as ex:
            raise InternalServerError(
            message=f"Error de eliminación del ingreso N°{income_id}. {ex}",
            exception_code='INCOME_UNHANDLED_ERROR'
            )
