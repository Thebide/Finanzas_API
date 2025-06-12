from typing import Annotated
from fastapi import APIRouter, Path, Query
from datetime import date, datetime

from src.schema.incomes_schema import newincomes_recuest, update_incomes_recuest, incomes_response, incomes_pagination
from .dependencies import incomes_controller

incomes_router = APIRouter(
    prefix= "/incomes",
    responses={
        401: {"Description": "Unatorized"},
        403: {"Description": "Forbidden"},
        500: {"Description": "Intarnal server error"},
        501: {"Description": "Not implemented"},
    }
)

@incomes_router.get(
    "", 
    name="Lista", 
    description="Lista de ingresos",
    response_description= "Retorna objeto con lista de resultados y la muestra",
    responses= {},
)
async def get_paginated(
    offset:Annotated[int, Query(gr=0)] = 0, 
    limit:Annotated[int, Query(ge=1 , le=50)] = 1,
    )-> incomes_pagination:
    return {
        "results": 
            [
            {
                "id": int,
                "name": str,
                "desciption": str,
                "quantity": int,
                "created": date,
                "update": date,
            }
            ],
        "metadata": {
            "concurrent_page": offset,
            "items_per_page": limit,
            "total_pages": int,
            "total_items": int,
        }
    }

@incomes_router.post(
        "",
        name= "Nuevo ingreso",
        description= "Creación y carga de ingresos",
        responses={
            201: {"Description":"Nuevo ingreso creado"},
            400: {"Description":"Revisar body request"},
        },      
)
async def create(new_incomes: newincomes_recuest) -> incomes_response:
    return await incomes_controller.create(new_incomes)


@incomes_router.get(
        '/{incomes_id}',
        name="ingresos por ID",
        responses={
            200: {"Description":"ingreso encontrado"},
            404: {"Description":"ingreso no encontrado"}
        },
    )
async def get_by_id(
    incomes_id: Annotated[int, Path(ge=1, description= "ID del ingreso a buscar", title="ID del ingreso")],
    ):
    # todo: filtrado por id
    return {
        "id": incomes_id,
        "name": str,
        "desciption": str,
        "quantity": int,
        "created": date,
        "update": date,
    }


@incomes_router.patch(
        '/{incomes_id}',
        name="Actualización de datos del ingreso",
        responses={
            200: {"Description":"ingreso actualizado"},
            404: {"Description":"ingreso no encontrado, imposible actualizar"}
        },
        )
async def update_by_id(
    incomes_id: Annotated[int, Path(ge=1, description= "ID del ingreso a buscar", title="ID del ingreso")],
    update_incomes: update_incomes_recuest,
    ) -> incomes_response:
    return {
        "id": incomes_id,
        "name": str,
        "desciption": str,
        "quantity": int,
        "created": date,
        "update": date,
    }


@incomes_router.delete(
        '/{incomes_id}',
        name="Borrar ingreso",
        status_code=204,
        responses={
            200: {"Description":"ingreso eliminado"},
            404: {"Description":"ingreso no encontrado, imposible de eliminar"}
        },
        )
async def delete_by_id(incomes_id: Annotated[int, Path(ge=1, description= "ID del ingreso a buscar", title="ID del ingreso")],) -> None:
    return None