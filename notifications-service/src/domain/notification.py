from enum import Enum
from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
from datetime import datetime


class TypeNotification(str, Enum):
    Mail = 'Mail'
    Text = 'Text'
    Whatsapp = 'Whatsapp'

class Status(str, Enum):
    New = 'New'
    Sended = 'Sended'
    Error = 'Error'
    Pending = 'Pending'
    
class Notification(BaseModel):
    _id: Optional[ObjectId] = None
    id: Optional[str] = None
    typeNotification: TypeNotification
    status: Status
    date : datetime = datetime.now() #https://stackoverflow.com/questions/7651064/create-an-isodate-with-pymongo
    address: str # puede ser nro, o email, etc, dependiendo del tipo de notificacion. 
    orderId: str
    message : str

    ## Email Revisar opcion:  https://www.mailjet.com/pricing/
    ## Revisar Whatsapp https://green-api.com/en/docs/sdk/python/   |  https://www.callmebot.com/es/blog/api-gratis-mensajes-whatsapp/  
    ##### https://www.google.com/search?q=send+message+whatsapp+free+api&sca_esv=8f089826b3e09913&rlz=1C5CHFA_enAR1121AR1121&biw=1728&bih=958&sxsrf=AHTn8zpK6WSLVb9KB3DlODp3EhS4SDTNyQ%3A1747519211390&ei=6wYpaJXEF8HT1sQPwYy5-QY&ved=0ahUKEwjV5dSuwKuNAxXBqZUCHUFGLm8Q4dUDCA8&uact=5&oq=send+message+whatsapp+free+api&gs_lp=Egxnd3Mtd2l6LXNlcnAiHnNlbmQgbWVzc2FnZSB3aGF0c2FwcCBmcmVlIGFwaTIGEAAYFhgeMgYQABgWGB4yCxAAGIAEGIYDGIoFMgsQABiABBiGAxiKBTILEAAYgAQYhgMYigUyCxAAGIAEGIYDGIoFMggQABiABBiiBDIFEAAY7wUyBRAAGO8FMgUQABjvBUjqDFDzAliRC3ABeACQAQCYAXKgAc0DqgEDNC4xuAEDyAEA-AEBmAIFoAKgA8ICChAAGLADGNYEGEeYAwCIBgGQBgiSBwMzLjKgB9MlsgcDMi4yuAebAw&sclient=gws-wiz-serp 
    ## Revisar sms https://rapidapi.com/collection/free-sms-apis
    
    def entity_mapping(notif) -> dict:
        res = {}
        notif_id = ''
        if notif is not None:
            if "_id" in notif:
                notif_id = str(notif["_id"])
            else:
                notif_id = notif["id"]
            res = {
                "id": notif_id,
                "typeNotification": notif["typeNotification"],
                "status": notif["status"],
                "date": notif["date"],
                "address": notif["address"],
                "orderId": notif["orderId"],
                "message": notif["message"]
            }
        return res

    def to_dict(self):
        return  {
                "id": self.id,
                "typeNotification": self.typeNotification,
                "status": self.status,
                "date": self.date,
                "address": self.address,
                "orderId": self.orderId,
                "message": self.message
            }