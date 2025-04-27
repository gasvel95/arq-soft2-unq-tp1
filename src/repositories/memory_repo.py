from typing import Optional
from domain.order import Order
from domain.order_repository_interface import OrderRepository
from domain.product import Product
from domain.product_repository_interface import ProductRepository
from domain.seller import Seller
from domain.seller_repository_interface import SellerRepository
from domain.user import User
from domain.user_repository_interface import UserRepository


class InMemoryUserRepo(UserRepository):
    def __init__(self): self.storage = {}
    def add(self, user: User): self.storage[user.id] = user
    def get(self, id: str) -> Optional[User]: return self.storage.get(id)

class InMemorySellerRepo(SellerRepository):
    def __init__(self): self.storage = {}
    def add(self, seller: Seller): self.storage[seller.id] = seller
    def get(self, id: str) -> Optional[Seller]: return self.storage.get(id)

class InMemoryProductRepo(ProductRepository):
    def __init__(self): self.storage = {}
    def add(self, product: Product): self.storage[product.id] = product
    def get(self, id: str) -> Optional[Product]: return self.storage.get(id)
    def update(self, product: Product): self.storage[product.id] = product

class InMemoryOrderRepo(OrderRepository):
    def __init__(self): self.storage = {}
    def add(self, order: Order): self.storage[order.id] = order