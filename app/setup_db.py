from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from os import environ

# from app.models import Phone, Base

BASE_DIR = Path(__file__).parent

TESTING = environ.get("TESTING")  # this will be used by pytest

if TESTING:
    engine = create_engine(
        f"sqlite:///{BASE_DIR.parent}/phones_test.db",
        connect_args={"check_same_thread": False},
        echo=True,
    )

else:
    engine = create_engine(
        f"sqlite:///{BASE_DIR.parent}/data/phones.db",
        connect_args={"check_same_thread": False},
        echo=False,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
