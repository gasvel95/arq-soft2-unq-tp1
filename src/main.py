from fastapi import FastAPI, HTTPException
from domain.order import Order
from domain.product import Product
from domain.seller import Seller
from domain.user import User
from repositories.mongo_order_repo import OrderRepositoryMongo
from repositories.mongo_product_repo import ProductRepositoryMongo
from repositories.mongo_seller_repo import SellerRepositoryMongo
from repositories.mongo_user_repo import UserRepositoryMongo
from services.order_service import OrderService
from services.product_service import ProductService
from services.seller_service import SellerService
from services.user_service import UserService

app = FastAPI()

#Create instances
user_repo = UserRepositoryMongo()
seller_repo = SellerRepositoryMongo()
product_repo = ProductRepositoryMongo()
order_repo = OrderRepositoryMongo()

user_service = UserService(user_repo)
seller_service = SellerService(seller_repo)
product_service = ProductService(product_repo)
order_service = OrderService(user_repo, product_repo, order_repo)

@app.post("/users")
def create_user(data: User):
    return user_service.create_user(data)

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id:str,data: User):
    u = user_service.update_user(user_id,data)
    return u.to_dict()

@app.get("/users/{user_id}", response_model= User)
def get_user(user_id: str):
    try:
        u = user_service.get_user(user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
    return u.to_dict()

@app.post("/sellers")
def create_seller(data: Seller):
    return seller_service.create_seller(data)

@app.put("/sellers/{seller_id}", response_model= Seller)
def create_seller(seller_id,data: Seller):
    s = seller_service.update_seller(seller_id,data)
    return s.to_dict()

@app.get("/sellers/{seller_id}", response_model=Seller)
def get_seller(seller_id: str):
    try:
        s = seller_service.get_seller(seller_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Seller not found")
    return s.to_dict()

@app.post("/products")
def create_product(data: Product):
    try:
        prod = product_service.create_product(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return prod

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: str,data: Product):
    try:
        prod = product_service.update_product(product_id,data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return prod

@app.get("/products/{product_id}", response_model= Product)
def get_product(product_id: str):
    try:
        p = product_service.get_product(product_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Product not found")
    return p.to_dict()

@app.post("/orders", response_model=Order)
def create_order(data: Order):
    try:
        order = order_service.process_order(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return order.to_dict()
