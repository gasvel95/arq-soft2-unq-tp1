from domain.notification_repository_inteface import NotificationRepository
from repositories.mongo_connect import db
from bson import ObjectId


class NotificationRepositoryImpl(NotificationRepository):
    def __init__(self):
        self.collection=db['notifications']
        
    def create(self, notification):
        notif_data = notification.to_dict()
        result = self.collection.insert_one(notif_data)
        notification.id = str(result.inserted_id)
        return notification
    
    def getById(self, id):
        data = self.collection.find_one({"_id": ObjectId(id)})
        if not data:
            raise Exception("Notification not found")
        return Notification.entity_mapping(data)
    
    def delete(self, id: str) -> None:
        self.collection.delete_one({"_id": ObjectId(id)})


