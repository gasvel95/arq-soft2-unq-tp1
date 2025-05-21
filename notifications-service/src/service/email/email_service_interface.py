from abc import ABC, abstractmethod
from typing import Optional
from src.domain.notification import Notification

class EmailService(ABC):
    
    @abstractmethod
    def sendEmail(self, toaddress:str, message_html:str, subject:str): ...
    
    
    