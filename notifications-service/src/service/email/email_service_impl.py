from src.service.email.email_service_interface import  EmailService
from mailjet_rest import Client

class EmailServiceImpl(EmailService):
    
    def __init__(self, mailjet: Client):
        super().__init__()
        self.mail_provider_service = mailjet
    
    
    def sendEmail(self, toaddress, message_html, subject) -> bool:
        
        data = {
            "FromEmail": "mportillo9@uvq.edu.ar",
            "FromName": "TP2 - ARQ2 - Notification Service",
            "Subject": subject,
#            "Html-part": '<div> Header </div> <br/> <h3>Dear passenger, welcome to <a href="https://www.mailjet.com/">Mailjet</a>!<br />May the delivery force be with you!',
            "Html-part" : message_html,
            "Recipients": [{"Email": toaddress}],
        }
        result =  self.mail_provider_service.send.create(data=data)        
        print(result.json())
        return result.status_code==200