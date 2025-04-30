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

@app.post("/users", response_model=User)
def create_user(data: User):
    return user_service.create_user(data)

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id:str,data: User):
    u = user_service.update_user(user_id,data)
    return u

@app.get("/users/{user_id}", response_model= User)
def get_user(user_id: str):
    try:
        u = user_service.get_user(user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
    return u

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    try:
        u = user_service.delete_user(user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
    return u

@app.post("/sellers", response_model=Seller)
def create_seller(data: Seller):
    return seller_service.create_seller(data)

@app.put("/sellers/{seller_id}", response_model= Seller)
def create_seller(seller_id,data: Seller):
    s = seller_service.update_seller(seller_id,data)
    return s

@app.get("/sellers/{seller_id}", response_model=Seller)
def get_seller(seller_id: str):
    try:
        s = seller_service.get_seller(seller_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Seller not found")
    return s

@app.delete("/sellers/{seller_id}")
def delete_seller(seller_id: str):
    try:
        seller_service.delete_seller(seller_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Seller not found")

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
    return p

@app.delete("/products/{product_id}")
def delete_product(product_id: str):
    try:
        product_service.delete_product(product_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Product not found")

@app.get("/products", response_model=list[Product])
def get_products(category: str | None = None, name: str | None = None, gte: int | None = None, lte: int | None = None):
    results = []
    if name != None:
        results = product_service.find_by_name(name)
    elif category != None:
        results = product_service.find_by_category(category)
    elif gte != None and lte != None:
        results = product_service.find_by_price(gte,lte)
    else:
        results = product_service.get_all()
    return results

@app.post("/orders", response_model=Order)
def create_order(data: Order):
    try:
        order = order_service.process_order(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return order

@app.get("/orders/{order_id}", response_model=Order)
def create_order(order_id: str):
    try:
        order = order_service.get_order(order_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return order
