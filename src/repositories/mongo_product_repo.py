from domain.product_repository_interface import ProductRepository
from domain.product import Product
from repositories.mongo_connect import db
from bson import ObjectId

class ProductRepositoryMongo(ProductRepository):
    def __init__(self):
        self.collection = db["products"]

    def add(self, product: Product) -> Product:
        product_data = product.to_dict()
        result = self.collection.insert_one(product_data)
        return str(result.inserted_id)

    def get(self, product_id: str) -> Product:
        data = self.collection.find_one({"_id": ObjectId(product_id)})
        if not data:
            raise Exception("Product not found")
        return Product(**data)

    def update(self, product: Product) -> Product:
        self.collection.update_one(
            {"_id": ObjectId(product._id)}, {"$set": product.to_dict()}
        )
        return product

    def delete(self, product_id: str) -> None:
        self.collection.delete_one({"_id": ObjectId(product_id)})

    def find_by_name(self, name: str) -> list[Product]:
        products = self.collection.find({"name": {"$regex": name, "$options": "i"}})
        return [Product(**p) for p in products]

    def find_by_category(self, category: str) -> list[Product]:
        products = self.collection.find({"category": category})
        return [Product(**p) for p in products]

    def filter_by_price(self, min_price: float, max_price: float) -> list[Product]:
        products = self.collection.find(
            {"price": {"$gte": min_price, "$lte": max_price}}
        )
        return [Product(**p) for p in products]
