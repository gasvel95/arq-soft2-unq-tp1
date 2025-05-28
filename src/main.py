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
order_service = OrderService(user_repo, product_repo, order_repo, seller_repo)


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
