from typing import Optional
from fastapi import Query
# from sqlalchemy.orm import Session

from app.setup_db import SessionLocal


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except:  # noqa
        db.rollback()
    finally:
        db.close()


class Page:
    def __init__(
        self,
        page: Optional[int] = Query(
            None,
            title="Страница",
            description="Укажите номер страницы для постраничного вывода (>0)",
            gt=0,
        ),
    ):
        self.value = page
