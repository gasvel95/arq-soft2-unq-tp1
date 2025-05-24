import uvicorn
from fastapi_websocket_rpc import RpcMethodsBase, WebsocketRPCEndpoint
from typing import Union
from fastapi import FastAPI
from src.repository.notification_repository import NotificationRepositoryImpl
from src.service.notification_service import NotificationService
from src.domain.notification import Notification
from src.service.email.email_service_impl import EmailServiceImpl
from mailjet_rest import Client
from pathlib import Path
import os
from dotenv import load_dotenv
from fastapi import Request
import json
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
mail_key = os.getenv("mail_key") 
mail_secret = os.getenv("mail_secret") 

app = FastAPI()

mailjet = Client(auth=(mail_key, mail_secret))
email_service=EmailServiceImpl(mailjet)
# initialize
notification_repo = NotificationRepositoryImpl()
notification_service = NotificationService(notification_repo,email_service)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/notifications", response_model=Notification)
def create_notification(data: Notification): 
    return notification_service.create_notification(data)

@app.post("/notifications/email", response_model=Notification)
async def send_notification_email(request: Request): 
    body = await request.body()
    print(body)
    data = json.loads(body)
    newNot = None
    result = notification_service.send_notification_user(data["userName"], data["userAddress"], data["action"],data["subject"],data["orderN"],data["productName"],data["quantity"],data["amount"] )
    if(result):
        newNot = Notification(typeNotification="Mail",status="Sended",address=data["userAddress"],orderId= data["orderN"])
    else:
        newNot = Notification(typeNotification="Mail",status="Sended",address=data["userAddress"],orderId= data["orderN"])    #notif = notification_service.create_notification(newNot)
    notif = notification_service.create_notification(newNot)
    return  notif


class NotificationServer(RpcMethodsBase):

    async def sendMail(self, notif: str)-> str:
        body =  notif
        print(body)
        data = json.loads(body)
        newNot = None
        result = notification_service.send_notification_user(data["userName"], data["userAddress"], data["action"],data["subject"],data["orderN"],data["productName"],data["quantity"],data["amount"] )
        if(result):
            newNot = Notification(typeNotification="Mail",status="Sended",address=data["userAddress"],orderId= data["orderN"])
        else:
            newNot = Notification(typeNotification="Mail",status="Error",address=data["userAddress"],orderId= data["orderN"])    #notif = notification_service.create_notification(newNot)
        notif = notification_service.create_notification(newNot)
        return newNot.status


endpoint = WebsocketRPCEndpoint(NotificationServer())
endpoint.register_route(app, "/ws")
uvicorn.run(app,host="0.0.0.0",port=9002)
