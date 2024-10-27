from fastapi import HTTPException


def validate_existence(item, item_id: int, item_name: str):
    if not item:
        raise HTTPException(status_code=404, detail=f'{item_name} con ID {item_id} no encontrado')


def validate_uniqueness_by_id(items, item_id: int, attributes: list):
    if not items:
        return
    for item in items:
        if item.id != item_id:
            for attribute, value in attributes.items():
                if getattr(item, attribute) == value:
                    raise HTTPException(status_code=400, detail=f'{attribute}: {value} ya está registrado')


def validate_uniqueness(items, attributes: list):
    if items is None:  # Verifica si la lista está vacía
        return
    for item in items:
        for attribute, value in attributes.items():
            if getattr(item, attribute) == value:
                raise HTTPException(status_code=400, detail=f'{attribute}: {value} ya está registrado')


def validate_uniqueness_single_by_id(item, item_id: int, attribute: str, value: int):
    if item is None:
        return  # No hacemos nada si el item es None
    if item.id != item_id:
        if getattr(item, attribute) == value:
            raise HTTPException(status_code=400, detail=f'{attribute}: {value} ya está registrado')


def validate_uniqueness_single(item, attribute: str, value):
    if item is None:
        return  # No hacemos nada si el item es None

    if getattr(item, attribute) == value:
        raise HTTPException(status_code=400, detail=f'{attribute}: {value} ya está registrado')