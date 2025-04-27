from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from repositories.memory_repo import InMemoryProductRepo, InMemorySellerRepo, InMemoryUserRepo
from services.order_service import OrderService
from services.product_service import ProductService
from services.seller_service import SellerService
from services.user_service import UserService

app = FastAPI()

# Instantiate in-memory repositories and services
user_repo = InMemoryUserRepo()
seller_repo = InMemorySellerRepo()
product_repo = InMemoryProductRepo()
sale_repo = InMemorySellerRepo()

user_service = UserService(user_repo)
seller_service = SellerService(seller_repo)
product_service = ProductService(product_repo)
order_service = OrderService(user_repo, product_repo, sale_repo)

# Schemas\ class UserCreate(BaseModel): first_name: str; last_name: str; email: str
class SellerCreate(BaseModel): company_name: str; email: str
class UserCreate(BaseModel): first_name: str; email: str; last_name: str
class ProductCreate(BaseModel): name: str; description: str; price: float; stock: int; seller_id: str
class SaleCreate(BaseModel): buyer_id: str; product_id: str; quantity: int

@app.post("/users")
def create_user(data: UserCreate):
    u = user_service.create_user(data.first_name, data.last_name, data.email)
    return u.to_dict()

@app.get("/users/{user_id}")
def get_user(user_id: str):
    try:
        u = user_service.get_user(user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
    return u.to_dict()

@app.post("/sellers")
def create_seller(data: SellerCreate):
    s = seller_service.create_seller(data.company_name, data.email)
    return s.to_dict()

@app.get("/sellers/{seller_id}")
def get_seller(seller_id: str):
    try:
        s = seller_service.get_seller(seller_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Seller not found")
    return s.to_dict()

@app.post("/products")
def create_product(data: ProductCreate):
    try:
        prod = product_service.create_product(data.name, data.description, data.price, data.stock, data.seller_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return prod.to_dict()

@app.get("/products/{product_id}")
def get_product(product_id: str):
    try:
        p = product_service.get_product(product_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Product not found")
    return p.to_dict()

@app.post("/orders")
def create_order(data: SaleCreate):
    try:
        order = order_service.process_sale(data.buyer_id, data.product_id, data.quantity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return order.to_dict()