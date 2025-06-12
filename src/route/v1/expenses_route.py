from typing import Annotated
from fastapi import APIRouter, Path, Query
from datetime import date, datetime

from src.schema.expenses_schema import newexpenses_recuest, update_expenses_recuest, expenses_response, expenses_pagination
from .dependencies import expenses_controller

expenses_router = APIRouter(
    prefix= "/expenses",
    responses={
        401: {"Description": "Unatorized"},
        403: {"Description": "Forbidden"},
        500: {"Description": "Intarnal server error"},
        501: {"Description": "Not implemented"},
    }
)

@expenses_router.get(
    "", 
    name="Lista", 
    description="Lista de gastos",
    response_description= "Retorna objeto con lista de resultados y la muestra",
    responses= {},
)
async def get_paginated(
    offset:Annotated[int, Query(ge=1)] = 1, 
    limit:Annotated[int, Query(ge=1 , le=50)] = 1,
    )-> expenses_pagination:
    return await expenses_controller.get_paginated(offset, limit)

@expenses_router.post(
        "",
        name= "Nuevo gasto",
        description= "Creación y carga de gastos",
        responses={
            201: {"Description":"Nuevo gasto creado"},
            400: {"Description":"Revisar body request"},
        },      
)
async def create(new_expenses: newexpenses_recuest) -> expenses_response:
    return await expenses_controller.create(new_expenses)


@expenses_router.get(
        '/{expense_id}',
        name="Gastos por ID",
        responses={
            200: {"Description":"Gasto encontrado"},
            404: {"Description":"Gasto no encontrado"}
        },
    )
async def get_by_id(
    expense_id: Annotated[int, Path(ge=1, description= "ID del gasto a buscar", title="ID del gasto")],
    ):
    # todo: filtrado por id
    return {
        "id": expense_id,
        "name": str,
        "desciption": str,
        "quantity": int,
        "fees": int,
        "payment_date": date,
        "estimated_next_payment_date" : date,
        "created": datetime,
        "Update": datetime,
    }


@expenses_router.patch(
        '/{expense_id}',
        name="Actualización de datos del gasto",
        responses={
            200: {"Description":"Gasto actualizado"},
            404: {"Description":"Gasto no encontrado, imposible actualizar"}
        },
        )
async def update_by_id(
    expense_id: Annotated[int, Path(ge=1, description= "ID del gasto a buscar", title="ID del gasto")],
    update_expense: update_expenses_recuest,
    ) -> expenses_response:
    return {
        "id": expense_id,
        "name": str,
        "desciption": str,
        "quantity": int,
        "fees": int,
        "payment_date": date,
        "estimated_next_payment_date": date,
        "created": datetime,
        "Update": datetime,
    }


@expenses_router.delete(
        '/{expense_id}',
        name="Borrar Gasto",
        status_code=204,
        responses={
            200: {"Description":"Gasto eliminado"},
            404: {"Description":"Gasto no encontrado, imposible de eliminar"}
        },
        )
async def delete_by_id(expense_id: Annotated[int, Path(ge=1, description= "ID del gasto a buscar", title="ID del gasto")],) -> None:
    return None