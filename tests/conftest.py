import pytest
import os
from sqlalchemy.orm import sessionmaker

from app.models import Base

os.environ['TESTING'] = 'TRUE'

from app.setup_db import engine  # noqa


@pytest.fixture(scope='module')
def db_migration():
    with engine.begin() as conn:
        Base.metadata.drop_all(conn)
        Base.metadata.create_all(conn)


@pytest.fixture()
def db_session(db_migration):
    with sessionmaker(autocommit=False, autoflush=False, bind=engine)() as db_session:
        yield db_session
        db_session.rollback()
