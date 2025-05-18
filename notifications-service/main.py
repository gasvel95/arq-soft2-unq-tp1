from typing import Union
from fastapi import FastAPI
from src.repository.notification_repository import NotificationRepositoryImpl
from src.service.notification_service import NotificationService
from src.domain.notification import Notification

app = FastAPI()

# initialize
notification_repo = NotificationRepositoryImpl()
notification_service = NotificationService(notification_repo)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/notifications", response_model=Notification)
def create_notification(data: Notification): 
    return notification_service.create_notification(data)