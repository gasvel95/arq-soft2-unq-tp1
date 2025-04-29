import uuid
from domain.price import Price
from domain.product import Product
from domain.product_repository_interface import ProductRepository


class ProductService:
    def __init__(self, product_repo: ProductRepository): self.product_repo = product_repo
    def create_product(self, product: Product) -> str:
        return self.product_repo.add(product)
    def get_product(self, id: str) -> Product:
        p = self.product_repo.get(id)
        if p is None: raise ValueError("Product not found")
        return p
    def update_product(self, prod_id: str, prod: Product) -> Product:
        prod._id = prod_id
        self.product_repo.update(prod)
        return prod