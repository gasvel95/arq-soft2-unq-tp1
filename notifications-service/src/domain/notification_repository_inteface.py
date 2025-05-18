from abc import ABC, abstractmethod
from typing import Optional
from src.domain.notification import Notification

class NotificationRepository(ABC):
    
    @abstractmethod
    def create(self, notification: Notification): ...
    
    @abstractmethod
    def getById(self, id: str): ...

    @abstractmethod
    def delete(self, id: str): ...