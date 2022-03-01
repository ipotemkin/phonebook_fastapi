import os
from http import HTTPStatus
import pytest
from app.models import Phone
from fixtures import data
from run import app
from fastapi.testclient import TestClient
from app.constants import ITEMS_ON_PAGE

client = TestClient(app)


class TestPhoneView:
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
        response = client.get("/phones/")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == phones

    def test_many_with_page(self):
        response = client.get("/phones/?page=1")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == data['phones'][:ITEMS_ON_PAGE]

    def test_one(self, db_session):
        response = client.get("/phones/1")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == data['phones'][0]

    def test_one_not_found(self, db_session):
        response = client.get("/phones/1000")
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'message': 'Not Found'}

    def test_many_with_name(self):
        response = client.get("/phones/?name=mes")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == [data['phones'][0]]

    def test_many_with_number(self):
        response = client.get("/phones/?phone_number=8")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == [data['phones'][0]]

    def test_create(self):
        payload = {
            "name": "Sarah",
            "phone_number": "+75555555",
        }
        response = client.post(
            "/phones",
            json=payload,
        )
        assert response.status_code == HTTPStatus.CREATED
        payload["id"] = 3
        assert response.json() == payload

    def test_update(self):
        payload = {
            "phone_number": "+75555555",
        }
        response = client.patch(
            "/phones/1",
            json=payload,
        )
        assert response.status_code == HTTPStatus.OK
        payload["id"] = data["phones"][0]["id"]
        payload["name"] = data["phones"][0]["name"]
        assert response.json() == payload

    def test_delete(self):
        response = client.delete("/phones/3")
        assert response.status_code == HTTPStatus.NO_CONTENT
        assert response.json() is None
