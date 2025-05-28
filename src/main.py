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

# RPC Server
class UserServer(RpcMethodsBase):
    async def getUser(self, id=""):
        return user_service.get_user(id)
    
    #TBD método para descontar el monto de la orden de la billetera del usuario
    async def buyOrder(self, id="", amount=0):
        return "TBD"

#Create instances
user_repo = UserRepositoryMongo()
user_service = UserService(user_repo)


#RPC Config server
endpoint = WebsocketRPCEndpoint(UserServer())
# add the endpoint to the app
endpoint.register_route(app, "/ws")
uvicorn.run(app,host="0.0.0.0",port=9001)