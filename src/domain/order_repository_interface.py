from abc import ABC, abstractmethod

from domain.order import Order

class OrderRepository(ABC):
    @abstractmethod
    def add(self, order: Order): ...