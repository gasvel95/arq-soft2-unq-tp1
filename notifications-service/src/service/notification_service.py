import uuid
from src.domain.notification_repository_inteface import NotificationRepository
from src.domain.notification import Notification
from src.service.email.email_service_interface import EmailService

class NotificationService():
    def __init__(self, notification_repo: NotificationRepository, email_service: EmailService): 
        self.notification_repo =  notification_repo
        self.email_service = email_service
    
    def create_notification(self, notification: Notification) -> Notification:
        return self.notification_repo.create(notification)
     
    def get_notification(self, id: str) -> Notification:
        try: 
            return self.notification_repo.getById(id)
        except:
            raise ValueError("Notification not Found")

    def delete_notification(self, id:str):
        return self.notification_repo.delete(id)
    
    def send_notification_email(self, toaddress, message_html, subject) -> bool:
        return self.email_service.sendEmail(toaddress,message_html,subject)
        
    def notification_seller(self,sellerName,selleraddress,subject,order_n,product_name,quantity, amount):
        body = f"<div> Estimado {sellerName} <br> Se ha registrado la siguiente venta Orden N° {order_n}. <br> Detalle: <br><ul><li>Producto: {product_name} </li><li>Cantidad: {quantity} </li><li>Monto: {amount} </li></ul> Ante cualquier duda enviar correo consultas@gmail.com<br><br>Saludos.<br>Atte.<br>"        
        print("======================>>>>>> " + body)
        return self.email_service.sendEmail(selleraddress, body,subject)
        
    ## TODO: agregar el servicio mailjet, el metodo de envio, y lo necesario.
    ## opt: crear super clase del servicio mailjet y que esta herede el comportamiento de envio de email. 
    