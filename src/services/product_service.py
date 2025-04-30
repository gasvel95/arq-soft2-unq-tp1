import uuid
from domain.price import Price
from domain.product import Product
from domain.product_repository_interface import ProductRepository


class ProductService:
    def __init__(self, product_repo: ProductRepository): self.product_repo = product_repo
    def create_product(self, product: Product) -> Product:
        return self.product_repo.add(product)
    def get_product(self, id: str) -> Product:
        try:
            return self.product_repo.get(id)
        except:
            raise ValueError("Product not found")

    def update_product(self, prod_id: str, prod: Product) -> Product:
        prod.id = prod_id
        self.product_repo.update(prod)
        return prod
    def find_by_name(self, name:str) -> list[Product]:
        return self.product_repo.find_by_name(name)
    def find_by_category(self, category:str) -> list[Product]:
        return self.product_repo.find_by_category(category)
    def find_by_price(self, gte: float, lte: float) -> list[Product]:
        return self.product_repo.filter_by_price(gte,lte)
    def get_all(self) -> list[Product]:
        return self.product_repo.get_all()
    def delete_product(self,id:str):
        return self.product_repo.delete(id)