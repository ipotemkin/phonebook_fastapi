import os
import pytest
from fastapi.testclient import TestClient

from fixtures import data
from run import app
from app.errors import NoContentError, ValidationError, BadRequestError, DatabaseError, NotFoundError
from app.models import Phone, PhoneBM
from app.crud import PhoneDAO

client = TestClient(app)


class TestPhoneCRUD:
    @pytest.fixture
    def phones(self, db_session):
        for i in data['phones']:
            db_session.add(Phone(**i))
            db_session.commit()
        return data['phones']

    @pytest.fixture
    def new_phone(self, db_session):
        obj = Phone(id=10, name='John', phone_number='+77777777')
        db_session.add(obj)
        db_session.commit()
        return obj

    def test_testing_is_true(self):
        assert os.environ.get("TESTING") == 'TRUE'

    def test_many(self, db_session, phones):
        response = PhoneDAO(db_session).get_all()
        assert response == phones

    def test_many_page(self, db_session):
        response = PhoneDAO(db_session).get_all(page=1)
        assert response == data["phones"][:2]

    def test_many_page_2(self, db_session):
        response = PhoneDAO(db_session).get_all(page=2)
        assert response == []

    def test_many_page_3(self, db_session):
        response = PhoneDAO(db_session).get_all(page=1, limit=1)
        assert response == [data["phones"][0]]

    def test_one(self, db_session):
        response = PhoneDAO(db_session).get_one(1)
        assert response == data["phones"][0]

    def test_one_not_found_error(self, db_session):
        with pytest.raises(NotFoundError):
            PhoneDAO(db_session).get_one(1000)

    def test_create(self, db_session):
        payload = {
            "name": "Sarah",
            "phone_number": "+75555555",
        }
        new_phone = Phone(**payload)
        res = PhoneDAO(db_session).create(payload)
        assert PhoneBM.from_orm(res).dict(exclude={"id"}) == PhoneBM.from_orm(new_phone).dict(exclude={"id"})
        assert res.id is not None
        assert res.id == 3

    def test_create_no_content(self, db_session):
        with pytest.raises(NoContentError):
            PhoneDAO(db_session).create(None)

    def test_create_validation_error(self, db_session):
        with pytest.raises(ValidationError):
            payload = {
                "name": "Dan",
                "phone": "123"
            }
            PhoneDAO(db_session).create(payload)

    def test_create_database_error(self, db_session):
        with pytest.raises(DatabaseError):
            payload = {
                "id": 1,
                "name": "Dan",
                "phone_number": "123"
            }
            PhoneDAO(db_session).create(payload)

    def test_update(self, db_session):
        payload = {
            "phone_number": "5",
        }
        res = PhoneDAO(db_session).update(payload, 1)
        assert res["phone_number"] == payload["phone_number"]

    def test_update_no_content(self, db_session):
        with pytest.raises(NoContentError):
            PhoneDAO(db_session).update(None, 1)

    def test_update_not_found_error(self, db_session):
        with pytest.raises(NotFoundError):
            payload = {
                "name": "Dan",
                "phone_number": "333"
            }
            PhoneDAO(db_session).update(payload, 100)

    def test_update_database_error(self, db_session):
        with pytest.raises(DatabaseError):
            payload = {
                "name": "Dan",
                "phone": "333"
            }
            PhoneDAO(db_session).update(payload, 1)

    def test_update_bad_request_error(self, db_session):
        with pytest.raises(BadRequestError):
            payload = {
                "id": 3,
                "name": "Dan",
                "phone": "333"
            }
            PhoneDAO(db_session).update(payload, 1)

    def test_delete(self, db_session):
        PhoneDAO(db_session).delete(3)

    def test_delete_not_found_error(self, db_session):
        with pytest.raises(NotFoundError):
            PhoneDAO(db_session).delete(200)

    def test_filter_name(self, db_session):
        response = PhoneDAO(db_session).get_all_by_filter({"name": "Mary"}, page=1)
        assert response == [data["phones"][1]]

    def test_filter__number(self, db_session):
        response = PhoneDAO(db_session).get_all_by_filter(
            {
                "phone_number": "+77777777",
            },
            page=1
        )
        assert response == [data["phones"][1]]

    def test_filter_name_number(self, db_session):
        response = PhoneDAO(db_session).get_all_by_filter(
            {
                "name": "Mary",
                "phone_number": "+77777777",
            },
            page=1
        )
        assert response == [data["phones"][1]]

    def test_filter_none(self, db_session):
        with pytest.raises(BadRequestError):
            PhoneDAO(db_session).get_all_by_filter(
                req=None,
                page=1
            )
