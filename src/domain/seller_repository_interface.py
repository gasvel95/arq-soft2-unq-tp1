from abc import ABC, abstractmethod
from typing import Optional

from domain.seller import Seller

class SellerRepository(ABC):
    @abstractmethod
    def add(self, seller: Seller): ...
    @abstractmethod
    def get(self, id: str) -> Optional[Seller]: ...
    @abstractmethod
    def update(self, seller: Seller): ...
    @abstractmethod
    def delete(self, id: str): ...