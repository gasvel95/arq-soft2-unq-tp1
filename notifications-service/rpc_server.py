from zero import ZeroServer
from src.repository.notification_repository import NotificationRepositoryImpl
from src.service.notification_service import NotificationService
from src.domain.notification import Notification
from src.service.email.email_service_impl import EmailServiceImpl
from mailjet_rest import Client
from pathlib import Path
import os
from dotenv import load_dotenv
import json

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
mail_key = os.getenv("mail_key") 
mail_secret = os.getenv("mail_secret") 

mailjet = Client(auth=(mail_key, mail_secret))
email_service=EmailServiceImpl(mailjet)
# initialize
notification_repo = NotificationRepositoryImpl()
notification_service = NotificationService(notification_repo,email_service)


app = ZeroServer(port=5559)

@app.register_rpc
def echo(msg: str) -> str:
    return msg

@app.register_rpc
async def hello_world() -> str:
    return "hello world"

@app.register_rpc
async def sendMail(notif: str)-> str:
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

if __name__ == "__main__":
    app.run()