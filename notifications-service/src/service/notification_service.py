import uuid
from src.domain.notification_repository_inteface import NotificationRepository
from src.domain.notification import Notification

class NotificationService:
    def __init__(self, notification_repo: NotificationRepository): 
        self.notification_repo =  notification_repo
    
    def create_notification(self, notification: Notification) -> Notification:
        return self.notification_repo.create(notification)
     
    def get_notification(self, id: str) -> Notification:
        try: 
            return self.notification_repo.getById(id)
        except:
            raise ValueError("Notification not Found")

    def delete_notification(self, id:str):
        return self.notification_repo.delete(id)