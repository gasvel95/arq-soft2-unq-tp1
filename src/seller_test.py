from typing import Any
from fastapi.testclient import TestClient
import pytest
import mongomock
from users_module import app
import repositories.mongo_connect as db

@pytest.fixture(autouse=True, scope='module')
def monkeymodule():
    with pytest.MonkeyPatch.context() as marketplace:
        yield marketplace

@pytest.fixture(scope="module")
def set_up_mongo(monkeymodule: pytest.MonkeyPatch):
    def test_client():
        return mongomock.MongoClient()
    monkeymodule.setattr(db, 'client', test_client)

@pytest.fixture(scope="module")
def set_up_db(monkeymodule: pytest.MonkeyPatch):
    def test_db(test_client):
        return test_client.db
    monkeymodule.setattr(db, 'db', test_db)

@pytest.fixture(scope="module")
def test_app(set_up_mongo: None, set_up_db: None):
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="module")
def set_up_data(test_app: TestClient):
    new_seller = {
                    "id": "68119ee78892ca8adcf46c3e",
                    "email": "company@test.com",
                    "company_name": "Company SA",
                }
    response_seller = test_app.post(url='/sellers', json=new_seller)
    return response_seller.json()

def test_new_seller(set_up_mongo: None, test_app: TestClient, set_up_data: Any):
    new_seller = {
                    "id": "68119ee78892ca8adcf46c3e",
                    "email": "company2@test",
                    "company_name": "Empresa SA",
                }
    response_seller = test_app.post(url='/sellers', json=new_seller)
    assert response_seller.status_code == 200
    assert response_seller.json()["company_name"] == "Empresa SA"

def test_get_seller(set_up_mongo: None, test_app: TestClient, set_up_data: Any):
    info_seller = set_up_data
    inserted_id = info_seller["id"]
    response = test_app.get(url='/sellers' + '/' + inserted_id)
    assert response.status_code == 200
    assert response.json()["company_name"] == "Company SA"

def test_get_seller_not_found(set_up_mongo: None, test_app: TestClient, set_up_data: Any):
    response = test_app.get(url='/sellers' + '/77779ee78892ca8adcf46c3e')
    assert response.status_code == 404


def test_update_seller(set_up_mongo: None, test_app: TestClient, set_up_data: Any):
    info_seller = set_up_data
    inserted_id = info_seller["id"]
    updated_seller = {
                        "id": "68119ee78892ca8adcf46c3e",
                        "email": "newmail@test.com",
                        "company_name": "Fulanos y asoc"
                    }
    response = test_app.put(url='/sellers' + '/' + inserted_id, json=updated_seller)
    assert response.status_code == 200
    assert response.json()["company_name"] == "Fulanos y asoc"
    assert response.json()["email"] == "newmail@test.com"
