from sqlalchemy.orm import Session
from app.setup_db import engine
from app.models import Base, Phone
from fixtures import data

# print("tables:")
# for i in Base.metadata.__dict__['tables']:
#     print(i)

db = Session(bind=engine)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

for phone in data['phones']:
    db.add(Phone(**phone))

db.commit()
