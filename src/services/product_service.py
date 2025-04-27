import uuid
from domain.price import Price
from domain.product import Product
from domain.product_repository_interface import ProductRepository


class ProductService:
    def __init__(self, product_repo: ProductRepository): self.product_repo = product_repo
    def create_product(self, name: str, description: str, price: float, stock: int, seller_id: str) -> Product:
        p = Product(str(uuid.uuid4()), name, description, Price(price), stock, seller_id)
        self.product_repo.add(p)
        return p
    def get_product(self, id: str) -> Product:
        p = self.product_repo.get(id)
        if p is None: raise ValueError("Product not found")
        return p