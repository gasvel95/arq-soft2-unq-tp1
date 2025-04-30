from abc import ABC, abstractmethod

from domain.order import Order

class OrderRepository(ABC):
    @abstractmethod
    def add(self, order: Order): ...
    @abstractmethod
    def update(self, order: Order): ...
    @abstractmethod
    def get(self, id: str) -> Order: ...