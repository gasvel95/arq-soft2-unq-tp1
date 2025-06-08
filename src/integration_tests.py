from multiprocessing import Process
from typing import Any
import requests
import pytest
import uvicorn
import logging
from orders_module import app
from users_module import app as app_us
from users_module import UserServer
from notifications_module import app as app_not
from notifications_module import NotificationServer
from fastapi_websocket_rpc import  WebsocketRPCEndpoint
from fastapi_websocket_rpc.logger import logging_config, LoggingModes, get_logger

URL_ORDERS = "http://localhost:9000"
URL_USERS = "http://localhost:9001"
URL_NOTIFICATIONS = "http://localhost:9002"

logging_config.set_mode(LoggingModes.UVICORN, logging.DEBUG)

#Setup 3 modules servers
def run_server1():
    uvicorn.run(app,host="localhost",port=9000)

def run_server2():
    endpoint = WebsocketRPCEndpoint(UserServer())
    endpoint.register_route(app_us, "/ws")
    uvicorn.run(app_us,host="localhost",port=9001)

def run_server3():
    endpoint = WebsocketRPCEndpoint(NotificationServer())
    endpoint.register_route(app_not, "/ws")
    uvicorn.run(app_not, host="localhost", port=9002)


# Start servers in different process
@pytest.fixture
def server():
    proc = Process(target=run_server1, args=(), daemon=True)
    proc.start()
    proc2 =Process(target=run_server2, args=(), daemon=True)
    proc2.start()
    proc3 =Process(target=run_server3, args=(), daemon=True)
    proc3.start()
    yield proc,proc2,proc3
    proc.kill() 
    proc2.kill() 
    proc3.kill()

@pytest.mark.asyncio
def test_order_creation(server):
    jsonBody = {    
                    "first_name": "Fulano",
                    "last_name": "Detal",
                    "email": "user@test.com"
                    }

    response = requests.post(url= URL_USERS + "/users",json=jsonBody)
    buyer_id = response.json()["id"]
    assert response.status_code == 200
    assert response.json()["first_name"] == "Fulano"

    charge = {
        "amount": 200,
        "currency": "USD"
    }
    response_charge = requests.put(url= URL_USERS + "/users/"+ buyer_id+"/charge",json=charge)
    assert response_charge.status_code == 200
    new_seller = {
                "email": "company@test.com",
                "company_name": "Company SA",
            }
    response_seller = requests.post(url=URL_USERS +"/sellers", json=new_seller)
    assert response_seller.status_code == 200
    seller_id = response_seller.json()["id"]

    new_prod = {
                    "name": "Heladera",
                    "description": "Ideal para pruebas",
                    "category": "Hogar",
                    "price": {"amount":10,"currency": "USD"},
                    "stock": 2,
                    "seller_id": response_seller.json()["id"]
                }
    response_product = requests.post(url=URL_ORDERS +"/products",json=new_prod)
    assert response_product.status_code == 200
    product_id = response_product.json()["id"]

    new_order = {
        "buyer_id": buyer_id,
        "quantity": 1,
        "product_id": product_id
    }
    response_order = requests.post(url=URL_ORDERS+"/orders",json=new_order)
    assert response_order.status_code == 200

    ##Cleanup

    response_prod_delete = requests.delete(url= URL_ORDERS +"/products/"+product_id)
    assert response_prod_delete.status_code == 200
    response_user_delete = requests.delete(url= URL_USERS +"/users/"+buyer_id)
    assert response_user_delete.status_code == 200
    response_seller_delete = requests.delete(url=URL_USERS +"/sellers/"+seller_id)
    assert response_seller_delete.status_code == 200

@pytest.mark.asyncio
def test_order_creation_error(server):
    jsonBody = {    
                    "first_name": "Fulano",
                    "last_name": "Detal",
                    "email": "user@test.com"
                    }

    response = requests.post(url= URL_USERS + "/users",json=jsonBody)
    buyer_id = response.json()["id"]
    assert response.status_code == 200
    assert response.json()["first_name"] == "Fulano"

    new_seller = {
                "email": "company@test.com",
                "company_name": "Company SA",
            }
    response_seller = requests.post(url=URL_USERS +"/sellers", json=new_seller)
    assert response_seller.status_code == 200
    seller_id = response_seller.json()["id"]

    new_prod = {
                    "name": "Heladera",
                    "description": "Ideal para pruebas",
                    "category": "Hogar",
                    "price": {"amount":10,"currency": "USD"},
                    "stock": 2,
                    "seller_id": response_seller.json()["id"]
                }
    response_product = requests.post(url=URL_ORDERS +"/products",json=new_prod)
    assert response_product.status_code == 200
    product_id = response_product.json()["id"]

    new_order = {
        "buyer_id": buyer_id,
        "quantity": 1,
        "product_id": product_id
    }
    response_order = requests.post(url=URL_ORDERS+"/orders",json=new_order)
    ## Error debido a fondos insuficientes
    assert response_order.status_code == 400

    ##Cleanup
    response_prod_delete = requests.delete(url= URL_ORDERS +"/products/"+product_id)
    assert response_prod_delete.status_code == 200
    response_user_delete = requests.delete(url= URL_USERS +"/users/"+buyer_id)
    assert response_user_delete.status_code == 200
    response_seller_delete = requests.delete(url=URL_USERS +"/sellers/"+seller_id)
    assert response_seller_delete.status_code == 200

@pytest.mark.asyncio
def test_user_CRUD(server):
    jsonBody = {    
                    "first_name": "Fulano",
                    "last_name": "Detal",
                    "email": "user@test.com"
                    }

    response = requests.post(url= URL_USERS + "/users",json=jsonBody)
    buyer_id = response.json()["id"]
    assert response.status_code == 200
    assert response.json()["first_name"] == "Fulano"
    assert response.json()["wallet"] == 0

    jsonUpdatedBody = {    
                "first_name": "Mengano",
                "last_name": "Detal",
                "email": "user@test.com"
                }

    response = requests.put(url= URL_USERS + "/users/"+buyer_id,json=jsonUpdatedBody)
    assert response.status_code == 200
    assert response.json()["first_name"] == "Mengano"
    assert response.json()["wallet"] == 0

    charge = {
        "amount": 200,
        "currency": "USD"
    }
    response = requests.put(url= URL_USERS + "/users/"+buyer_id+"/charge",json=charge)
    assert response.status_code == 200
    assert response.json()["first_name"] == "Mengano"
    assert response.json()["wallet"] == 200

    discharge = {
        "amount": 100,
        "currency": "USD"
    }
    response = requests.put(url= URL_USERS + "/users/"+buyer_id+"/discharge",json=discharge)
    assert response.status_code == 200
    assert response.json()["first_name"] == "Mengano"
    assert response.json()["wallet"] == 100

    ##Cleanup
    response_user_delete = requests.delete(url= URL_USERS +"/users/"+buyer_id)
    assert response_user_delete.status_code == 200

    response = requests.get(url=URL_USERS+"/users/"+buyer_id)
    assert response.status_code == 404


@pytest.mark.asyncio
def test_seller_CRUD(server):
    jsonBody = {    
                    "company_name": "Fulano SA",
                    "email": "user@test.com"
                    }

    response = requests.post(url= URL_USERS + "/sellers",json=jsonBody)
    buyer_id = response.json()["id"]
    assert response.status_code == 200
    assert response.json()["company_name"] == "Fulano SA"
    assert response.json()["wallet"] == 0

    jsonUpdatedBody = {    
                "company_name": "Mengano SA",
                "email": "user@test.com"
                }

    response = requests.put(url= URL_USERS + "/sellers/"+buyer_id,json=jsonUpdatedBody)
    assert response.status_code == 200
    assert response.json()["company_name"] == "Mengano SA"
    assert response.json()["wallet"] == 0

    charge = {
        "amount": 200,
        "currency": "USD"
    }
    response = requests.put(url= URL_USERS + "/sellers/"+buyer_id+"/charge",json=charge)
    assert response.status_code == 200
    assert response.json()["company_name"] == "Mengano SA"
    assert response.json()["wallet"] == 200

    discharge = {
        "amount": 100,
        "currency": "USD"
    }
    response = requests.put(url= URL_USERS + "/sellers/"+buyer_id+"/discharge",json=discharge)
    assert response.status_code == 200
    assert response.json()["company_name"] == "Mengano SA"
    assert response.json()["wallet"] == 100

    ##Cleanup
    response_user_delete = requests.delete(url= URL_USERS +"/sellers/"+buyer_id)
    assert response_user_delete.status_code == 200

    response = requests.get(url=URL_USERS+"/sellers/"+buyer_id)
    assert response.status_code == 404