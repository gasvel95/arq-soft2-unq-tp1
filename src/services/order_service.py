import json
from domain.order import Order
from domain.order_repository_interface import OrderRepository
from domain.product import Product
from domain.user import User
from domain.product_repository_interface import ProductRepository

class OrderService:
    def __init__(self, product_repo: ProductRepository, order_repo: OrderRepository):
        self.product_repo = product_repo
        self.order_repo = order_repo
        
    def get_order(self, id: str) -> Order:
        try:
            return self.order_repo.get(id)
        except:
            raise ValueError('Order not found')
    def  process_order(self, user:User, order: Order) -> Order:
        if user is None: raise ValueError("User not found")
        buyer = json.loads(user.replace("'", "\""))
        product = Product(**self.product_repo.get(order.product_id))
        if product is None: raise ValueError("Product not found")
        product.reduce_stock(order.quantity)
        if product.stock <= 0:
            raise ValueError("Insufficient stock")
        order.calculate_total(product.price)
        if order.total.amount  > buyer["wallet"]:
            raise ValueError("Insufficient funds")
        self.product_repo.update(product)
        self.order_repo.add(order)
        return order
    
