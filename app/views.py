from typing import Optional

from fastapi import APIRouter, Depends, Query, Path, status, Response
from sqlalchemy.orm import Session

from app.crud import PhoneDAO
from app.models import PhoneBM, PhoneUpdateBM
from app.dependencies import get_db, Page

router = APIRouter(prefix="/phones", tags=["phones"])


@router.get("", summary="Получить все телефоны")
@router.get("/", include_in_schema=False)  # alternative endpoint
async def phones_get_all(
    name: Optional[str] = Query(None, title="Имя", description="Поиск по имени"),
    phone_number: Optional[str] = Query(None, title="Номер телефона", description="Поиск по номеру телефона"),
    page=Depends(Page),
    db: Session = Depends(get_db),
):
    """
    Получить все телефоны. Можно в качестве фильтра, задать имя или номер (часть имени / номера)
    """
    query_d = {}
    if name:
        query_d["name"] = name
    if phone_number:
        query_d["phone_number"] = phone_number

    if query_d:
        return PhoneDAO(db).get_all_by_filter(query_d, page=page.value)

    return PhoneDAO(db).get_all(page=page.value)


@router.get("/{pk}", summary="Получить запись по ID")
@router.get("/{pk}/", include_in_schema=False)  # alternative endpoint
async def phones_get_one(
    pk: int = Path(..., title="ID записи", description="Укажите ID записи"),
    db: Session = Depends(get_db),
):
    """
    Получить запись по ID:

    - **pk**: ID записи
    """
    return PhoneDAO(db).get_one(pk)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Добавить телефон",
    response_description="The created item",
)
@router.post(
    "/",  # alternative endpoint
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False
)
async def phone_post(phone: PhoneBM, response: Response, db: Session = Depends(get_db)):
    """
    Добавить телефон:

    - **id**: ID пользователя - целое число (необязательный параметр)
    - **name**: имя пользователя
    - **phone_number**: номер телефона
    """
    new_obj = PhoneDAO(db).create(phone.dict())
    response.headers["Location"] = f"{router.prefix}/{new_obj.id}"
    return PhoneBM.from_orm(new_obj).dict()


@router.patch("/{pk}", summary="Изменить телефон")
@router.patch("/{pk}/", include_in_schema=False)  # alternative endpoint
async def phone_update(
    phone: PhoneUpdateBM,
    pk: int = Path(..., title="ID записи", description="Укажите ID записи"),
    db: Session = Depends(get_db),
):
    """
    Изменить телефон:

    - **name**: изменить имя пользователя
    - **phone_number**: изменить телефон
    """
    return PhoneDAO(db).update(phone.dict(exclude_unset=True), pk)


@router.delete(
    "/{pk}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить телефон",
)
@router.delete(
    "/{pk}/",  # alternative endpoint
    status_code=status.HTTP_204_NO_CONTENT,
    include_in_schema=False,
)
async def phone_delete(
    pk: int = Path(..., title="ID записи", description="Укажите ID записи"),
    db: Session = Depends(get_db),
):
    """
    Удалить телефон:

    - **pk**: ID записи
    """
    return PhoneDAO(db).delete(pk)
