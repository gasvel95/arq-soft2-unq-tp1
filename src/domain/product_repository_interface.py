from abc import ABC, abstractmethod
from typing import Optional

from domain.product import Product

class ProductRepository(ABC):
    @abstractmethod
    def add(self, product: Product): ...
    @abstractmethod
    def get(self, id: str) -> Optional[Product]: ...
    @abstractmethod
    def update(self, product: Product): ...