from typing import Optional, List

from app.errors import (
    NotFoundError,
    NoContentError,
    BadRequestError,
    DatabaseError,
    ValidationError,
)
from app.constants import ITEMS_ON_PAGE
from app.models import Phone, PhoneBM


def paginate(page: Optional[int], limit: Optional[int]) -> tuple[Optional[int], Optional[int]]:
    """
    calculates start_at (~offset) and makes limit None if page is None
    (needed to apply offset/limit in sqlalchemy)
    """

    if page is None:
        start_at = 0
        limit = None
    else:
        start_at = (page - 1) * limit

    return start_at, limit


class PhoneDAO:
    def __init__(self, session):
        self.session = session
        self.model = Phone
        self.schema = PhoneBM   # if validation needed while creating/updating a record

    def get_all(self, page: Optional[int] = None, limit: Optional[int] = ITEMS_ON_PAGE) -> List[dict]:
        start_at, limit = paginate(page, limit)
        objs = self.session.query(self.model).offset(start_at).limit(limit).all()
        return [self.schema.from_orm(obj).dict() for obj in objs]

    def get_one(self, uid: int) -> dict:
        if not (obj := self.session.query(self.model).get(uid)):
            raise NotFoundError
        return self.schema.from_orm(obj).dict()

    def create(self, new_obj: dict):
        if not new_obj:
            raise NoContentError

        try:
            obj = self.model(**new_obj)
        except Exception:
            raise ValidationError

        try:
            self.session.add(obj)
            self.session.commit()
        except Exception as e:
            print(e)
            raise DatabaseError
        return obj

    def update(self, new_obj: dict, uid: int) -> dict:
        if not new_obj:
            raise NoContentError

        # if exists id in new_obj should be equal to uid
        if ("id" in new_obj) and (uid != new_obj["id"]):
            raise BadRequestError

        # checking existence of the record
        q = self.session.query(self.model).filter(self.model.id == uid)
        if not q:
            raise NotFoundError

        try:
            q.update(new_obj)
            self.session.commit()
        except Exception:
            raise DatabaseError
        return self.get_one(uid)

    def delete(self, uid: int) -> None:
        if not (obj := self.session.query(self.model).get(uid)):
            raise NotFoundError
        try:
            self.session.delete(obj)
            self.session.commit()
        except Exception:
            raise DatabaseError

    def get_all_by_filter(self, req: dict, page: Optional[int] = None, limit: Optional[int] = ITEMS_ON_PAGE) -> list:
        if not req:
            raise BadRequestError

        start_at, limit = paginate(page, limit)

        sql = f"select * from phone where "
        sql_lst = []
        if 'name' in req:
            sql_lst.append(f"lower(name) like '%{req['name'].lower()}%'")
        if 'phone_number' in req:
            sql_lst.append(f"phone_number like '%{req['phone_number']}%'")
        if sql_lst:
            sql += " and ".join(sql_lst)

        if limit:
            sql += f" limit {limit} offset {start_at}"

        res = self.session.execute(sql).all()

        return [self.schema.from_orm(obj).dict() for obj in res]
