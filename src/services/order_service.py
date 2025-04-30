import uuid
from domain.order import Order
from domain.order_repository_interface import OrderRepository
from domain.product import Product
from domain.product_repository_interface import ProductRepository
from domain.user_repository_interface import UserRepository


class OrderService:
    def __init__(self, user_repo: UserRepository, product_repo: ProductRepository, order_repo: OrderRepository):
        self.user_repo = user_repo
        self.product_repo = product_repo
        self.order_repo = order_repo
    def get_order(self, id: str) -> Order:
        try:
            return self.order_repo.get(id)
        except:
            raise ValueError('Order not found')
    def process_order(self, order: Order) -> Order:
        user = self.user_repo.get(order.buyer_id)
        if user is None: raise ValueError("User not found")
        product = Product(**self.product_repo.get(order.product_id))
        if product is None: raise ValueError("Product not found")
        product.reduce_stock(order.quantity)
        self.product_repo.update(product)
        order.calculate_total(product.price)
        self.order_repo.add(order)
        return order