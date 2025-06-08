import asyncio
import json
from fastapi import FastAPI, HTTPException
from domain.price import Price
from domain.seller import Seller
from domain.user import User
from repositories.mongo_seller_repo import SellerRepositoryMongo
from repositories.mongo_user_repo import UserRepositoryMongo
from services.seller_service import SellerService
from services.user_service import UserService
import uvicorn
from fastapi_websocket_rpc import RpcMethodsBase, WebsocketRPCEndpoint, WebSocketRpcClient

PORT = 9002

app = FastAPI()

#Create instances
user_repo = UserRepositoryMongo()
seller_repo = SellerRepositoryMongo()

user_service = UserService(user_repo)
seller_service = SellerService(seller_repo)



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

@app.put("/users/{user_id}/charge", response_model=User)
def charge_wallet_user(user_id: str,data: Price):
    return user_service.charge_amount(user_id,data)

@app.put("/users/{user_id}/discharge", response_model=User)
def discharge_wallet_user(user_id: str,data: Price):
    return user_service.discount_amount(user_id,data)

@app.post("/sellers", response_model=Seller)
def create_seller(data: Seller):
    return seller_service.create_seller(data)

@app.put("/sellers/{seller_id}/charge", response_model=Seller)
def charge_wallet_seller(seller_id: str,data: Price):
    return seller_service.charge_amount(seller_id,data)

@app.put("/sellers/{seller_id}/discharge", response_model=Seller)
def discharge_wallet_seller(seller_id: str,data: Price):
    return seller_service.discount_amount(seller_id,data)

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


async def run_client(uri , notif:str)->object:
    async with WebSocketRpcClient(uri, RpcMethodsBase()) as client:
        print(f"notifi---> {notif}")
        response = await client.other.sendMail(notif=notif)
        return response.result
    
def util_notification_obj(name:str, email:str, action:str,subject:str, orderId:str,quantity:int,amount:int,curr:str,productName:str)->dict :  
    return {
        "userName":name, 
        "userAddress":email, 
        "action": action, 
        "subject": subject,
        "orderN": orderId,
        "productName": productName,
        "quantity": quantity, 
        "amount": f"{amount}  {curr} "  
    } 

class UserServer(RpcMethodsBase):
    async def getUser(self, id=""):
        return user_service.get_user(id)
    
    async def notifySeller(self, id="",order=None,productName=""):
        seller  =  seller_service.get_seller(id)
        notif = util_notification_obj(name=seller['company_name'], email=seller['email'], action="Venta",subject="Venta de producto", orderId=order["id"], quantity=order["quantity"], amount=order["total"]["amount"], curr=order["total"]["currency"],productName=productName)
        notifi_seller = await run_client(f"ws://localhost:{PORT}/ws", json.dumps(notif))
        return notifi_seller
    
    async def notifyUser(self, id="",order=None, productName=""):
        user = user_service.get_user(id)
        notif = util_notification_obj(name=user['first_name'], email=user['email'], action="Compra",subject="Compra de producto", orderId=order["id"], quantity=order["quantity"], amount=order["total"]["amount"], curr=order["total"]["currency"],productName=productName)
        notifi_seller = await run_client(f"ws://localhost:{PORT}/ws", json.dumps(notif))
        return notifi_seller
    #Método para descontar el monto de la orden de la billetera del usuario
    async def buyOrder(self, user_id="",seller_id="", amount=None):
        user = user_service.discount_amount(user_id,Price(**amount))
        seller = seller_service.charge_amount(seller_id,Price(**amount))
        return None

if __name__ == "__main__":
    #RPC Config server
    endpoint = WebsocketRPCEndpoint(UserServer())
    # add the endpoint to the app
    endpoint.register_route(app, "/ws")
    uvicorn.run(app,host="0.0.0.0",port=9001)
