from fastapi import FastAPI, HTTPException
from domain.seller import Seller
from domain.user import User
from repositories.mongo_seller_repo import SellerRepositoryMongo
from repositories.mongo_user_repo import UserRepositoryMongo
from services.seller_service import SellerService
from services.user_service import UserService
import uvicorn
from fastapi_websocket_rpc import RpcMethodsBase, WebsocketRPCEndpoint

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


class UserServer(RpcMethodsBase):
    async def getUser(self, id=""):
        return user_service.get_user(id)
    
    #TBD método para descontar el monto de la orden de la billetera del usuario
    async def buyOrder(self, id="", amount=0):
        return "TBD"

if __name__ == "__main__":
    #RPC Config server
    endpoint = WebsocketRPCEndpoint(UserServer())
    # add the endpoint to the app
    endpoint.register_route(app, "/ws")
    uvicorn.run(app,host="0.0.0.0",port=9001)
