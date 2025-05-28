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

@pytest.fixture()
def test_app(set_up_mongo: None, set_up_db: None):
    with TestClient(app) as test_client:
        yield test_client
        
def test_new_users(set_up_mongo: None, test_app: TestClient):
    new_user = {
                    "id": "idtest",
                    "first_name": "Fulano",
                    "last_name": "Detal",
                    "email": "user@test.com"
                }
    
    response = test_app.post(url='/users', json=new_user)
    assert response.status_code == 200
    assert response.json()["first_name"] == "Fulano"


def test_get_user(set_up_mongo: None, test_app: TestClient):
    new_user = {
                    "id": "idtest",
                    "first_name": "Fulano",
                    "last_name": "Detal",
                    "email": "user@test.com"
                }
    
    response_post = test_app.post(url='/users', json=new_user)
    inserted_id = response_post.json()["id"]
    response = test_app.get(url='/users' + '/' + inserted_id)
    assert response.status_code == 200
    assert response.json()["first_name"] == "Fulano"


def test_update_user(set_up_mongo: None, test_app: TestClient):
    new_user = {
                    "id": "idtest",
                    "first_name": "Fulano",
                    "last_name": "Detal",
                    "email": "user@test.com"
                }
    
    response_post = test_app.post(url='/users', json=new_user)
    inserted_id = response_post.json()["id"]
    updated_user = {
                        "id": "idtest",
                        "first_name": "nuevo Fulano",
                        "last_name": "Detal",
                        "email": "user@test.com"
                    }
    response = test_app.put(url='/users' + '/' + inserted_id, json=updated_user)
    assert response.status_code == 200
    assert response.json()["first_name"] == "nuevo Fulano"
