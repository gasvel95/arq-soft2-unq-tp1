from fastapi import FastAPI, HTTPException
import uvicorn
from domain.order import Order
from domain.product import Product
from repositories.mongo_order_repo import OrderRepositoryMongo
from repositories.mongo_product_repo import ProductRepositoryMongo
from services.order_service import OrderService
from services.product_service import ProductService
import asyncio
from fastapi_websocket_rpc import RpcMethodsBase, WebSocketRpcClient

app = FastAPI()
PORT = 9001

product_repo = ProductRepositoryMongo()
order_repo = OrderRepositoryMongo()
product_service = ProductService(product_repo)
order_service = OrderService(product_repo, order_repo)

# RPC config client
async def run_client(uri,user_id):
    async with WebSocketRpcClient(uri, RpcMethodsBase()) as client:
        response = await client.other.getUser(id=user_id)
        return response.result
    
# RPC to discount amount from user's wallet
async def purchase_order(uri,user_id,seller_id, amount):
    async with WebSocketRpcClient(uri,RpcMethodsBase()) as client:
        response = await client.other.buyOrder(user_id=user_id,seller_id=seller_id, amount=amount)
        return response.result
    
async def notify_user(uri,user_id, order, product_name):
    async with WebSocketRpcClient(uri,RpcMethodsBase()) as client:
        response = await client.other.notifyUser(id=user_id, order=order,productName=product_name )
        return response.result
    
async def notify_seller(uri,user_id, order,product_name):
    async with WebSocketRpcClient(uri,RpcMethodsBase()) as client:
        response = await client.other.notifySeller(id=user_id, order=order,productName=product_name)
        return response.result

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
        user = asyncio.run(run_client(f"ws://localhost:{PORT}/ws",data.buyer_id))
        order = order_service.process_order(user,data)
        product = product_service.get_product(order.product_id)
        if order != None:
            asyncio.run(purchase_order(f"ws://localhost:{PORT}/ws",order.buyer_id,product["seller_id"],order.total))
            asyncio.run(notify_user(f"ws://localhost:{PORT}/ws",order.buyer_id,order,product["name"]))
            asyncio.run(notify_seller(f"ws://localhost:{PORT}/ws",product["seller_id"],order,product["name"]))
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



if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=9000)