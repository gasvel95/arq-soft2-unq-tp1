from typing import Any
from fastapi.testclient import TestClient
import pytest
import mongomock
from main import app
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
    new_user = {
                    "id": "11119ee78892ca8adcf46c3e",
                    "first_name": "Fulano",
                    "last_name": "Detal",
                    "email": "pruebas@test.com"
                }
    
    response_user = test_app.post(url='/users', json=new_user)
    new_seller = {
                    "id": "22229ee78892ca8adcf46c3e",
                    "email": "company@test.com",
                    "company_name": "Company SA"
                }
    response_seller = test_app.post(url='/sellers', json=new_seller)
    print(response_seller.json())
    new_prod = {
                    "id": "33339ee78892ca8adcf46c3e",
                    "name": "Heladera",
                    "description": "Ideal para pruebas",
                    "category": "Hogar",
                    "price": {"amount":10,"currency": "USD"},
                    "stock": 2,
                    "seller_id": response_seller.json()["id"]
                }
    response_prod = test_app.post(url='/products', json=new_prod)
    new_order = {
                    "id": "44449ee78892ca8adcf46c3e",
                    "buyer_id": response_user.json()["id"],
                    "product_id": response_prod.json()["id"],
                    "quantity": 1
                    
                }
    response_order = test_app.post(url='/orders', json=new_order)
    return response_user.json(), response_prod.json(), response_order.json()

def test_new_order(set_up_mongo: None, test_app: TestClient, set_up_data: Any):
    info_user, info_prod, info_order = set_up_data
    new_order = {
                    "id": "44449ee78892ca8adcf46c3e",
                    "buyer_id": info_user["id"],
                    "product_id": info_prod["id"],
                    "quantity": 1
                }
    response = test_app.post(url='/orders', json=new_order)
    assert response.status_code == 200
    assert response.json()["buyer_id"] == info_user["id"]
    assert response.json()["product_id"] == info_prod["id"]
    assert response.json()["total"] == {"amount": 10, "currency": "USD"}

def test_get_order(set_up_mongo: None, test_app: TestClient, set_up_data: Any):
    info_user, info_prod,info_order = set_up_data
    inserted_id = info_order["id"]
    print(inserted_id)
    response = test_app.get(url='/orders' + '/' + inserted_id)
    assert response.status_code == 200
    assert response.json()["buyer_id"] == info_user["id"]

def test_get_order_not_found(set_up_mongo: None, test_app: TestClient, set_up_data: Any):
    response = test_app.get(url='/orders' + '/99999ee78892ca8adcf46c3e')
    assert response.status_code == 404
