from abc import ABC, abstractmethod
from typing import Optional

from domain.user import User

class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User): ...
    @abstractmethod
    def get(self, id: str) -> Optional[User]: ...
    @abstractmethod
    def update(self,user:User): ...