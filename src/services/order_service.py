import uuid
from domain.order import Order
from domain.order_repository_interface import OrderRepository
from domain.product_repository_interface import ProductRepository
from domain.user_repository_interface import UserRepository


class OrderService:
    def __init__(self, user_repo: UserRepository, product_repo: ProductRepository, order_repo: OrderRepository):
        self.user_repo = user_repo
        self.product_repo = product_repo
        self.order_repo = order_repo
    def process_order(self, buyer_id: str, product_id: str, quantity: int) -> Order:
        user = self.user_repo.get(buyer_id)
        if user is None: raise ValueError("User not found")
        product = self.product_repo.get(product_id)
        if product is None: raise ValueError("Product not found")
        product.reduce_stock(quantity)
        self.product_repo.update(product)
        order = Order(str(uuid.uuid4()), buyer_id, product, quantity)
        self.order_repo.add(order)
        return order