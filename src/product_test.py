from typing import Any
from fastapi.testclient import TestClient
import pytest
import mongomock
from users_module import app as app_usmd
from orders_module import app as app_op
import repositories.mongo_connect as db

@pytest.fixture(autouse=True, scope='module')
def monkeymodule():
    with pytest.MonkeyPatch.context() as mp:
        yield mp

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
    with TestClient(app_usmd) as test_client:
        yield test_client

@pytest.fixture(scope="module")
def test_app_prod(set_up_mongo: None, set_up_db: None):
    with TestClient(app_op) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def set_up_data(test_app: TestClient):
    new_seller = {
                    "id": "77779ee78892ca8adcf46c3e",
                    "email": "company@test.com",
                    "company_name": "Company SA"
                }
    response = test_app.post(url='/sellers', json=new_seller)
    return response.json()
    
def test_new_product(set_up_mongo: None, test_app_prod: TestClient, set_up_data: dict):
    seller_id = set_up_data["id"]
    new_prod = {
                    "id": "11119ee78892ca8adcf46c3e",
                    "name": "Heladera",
                    "description": "Heladera ideal para pruebas",
                    "category": "Hogar",
                    "price": {"amount": 15, "currency": "USD"},
                    "stock": 1,
                    "seller_id": seller_id
                }
    response = test_app_prod.post(url='/products', json=new_prod)
    assert response.status_code == 200
    assert response.json()["name"] == "Heladera"

def test_update_product(set_up_mongo: None, test_app_prod: TestClient, set_up_data: dict):
    seller_id = set_up_data["id"]
    new_prod = {
                    "id": "idprod",
                    "name": "Heladera",
                    "description": "Heladera ideal para pruebas",
                    "category": "Hogar",
                    "price": {"amount": 15, "currency": "USD"},
                    "stock": 1,
                    "seller_id": seller_id
                }
    response_post = test_app_prod.post(url='/products', json=new_prod)
    inserted_id = response_post.json()["id"]
    updated_prod = {
                        "id": "idprod",
                        "name": "Heladera premium",
                        "description": "Heladera ideal para pruebas",
                        "category": "Hogar",
                        "price": {"amount": 10, "currency": "USD"},
                        "stock": 1,
                        "seller_id": seller_id
                    }
    response = test_app_prod.put(url='/products' + '/' + inserted_id, json=updated_prod)
    assert response.status_code == 200
    assert response.json()["name"] == "Heladera premium"

def test_get_all_products(set_up_mongo: None, test_app_prod: TestClient, set_up_data: dict):
    seller_id = set_up_data["id"]
    new_prod = {
                    "id": "idprod",
                    "name": "Heladera",
                    "description": "Heladera ideal para pruebas",
                    "category": "Hogar",
                    "price": {"amount": 15, "currency": "USD"},
                    "stock": 1,
                    "seller_id": seller_id
                }
    response = test_app_prod.post(url='/products', json=new_prod)
    response = test_app_prod.get(url='/products')
    assert response.status_code == 200
    assert response.json() != []

def test_get_product(set_up_mongo: None, test_app_prod: TestClient, set_up_data: dict):
    seller_id = set_up_data["id"]
    new_prod = {
                    "id": "idprod",
                    "name": "Heladera",
                    "description": "Heladera ideal para pruebas",
                    "category": "Hogar",
                    "price": {"amount": 15, "currency": "USD"},
                    "stock": 1,
                    "seller_id": seller_id
                }
    response_post = test_app_prod.post(url='/products', json=new_prod)
    inserted_id = response_post.json()["id"]
    response = test_app_prod.get(url='/products' + '/' + inserted_id)
    assert response.status_code == 200
    assert response.json()["name"] == "Heladera"


def test_delete_product(set_up_mongo: None, test_app_prod: TestClient, set_up_data: dict):
    seller_id = set_up_data["id"]
    new_prod = {
                    "id": "idprod",
                    "name": "Heladera",
                    "description": "Heladera ideal para pruebas",
                    "category": "Hogar",
                    "price": {"amount": 15, "currency": "USD"},
                    "stock": 1,
                    "seller_id": seller_id
                }
    response_post = test_app_prod.post(url='/products', json=new_prod)
    inserted_id = response_post.json()["id"]
    response = test_app_prod.delete(url='/products' + '/' + inserted_id)
    assert response.status_code == 200