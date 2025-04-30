from enum import Enum
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel
from domain.price import Price

class CategoryEnum(str,Enum):
    Electrodomesticos = 'Electrodomesticos'
    Vehiculos = 'Vehiculos'
    Hogar = 'Hogar'
    Tecnologia = 'Tecnologia'
    Almacen = 'Almacen'


class Product(BaseModel):
    _id: Optional[ObjectId] = None
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    price: Price
    stock: int
    category: CategoryEnum
    seller_id: str


    def reduce_stock(self, quantity: int):
        if quantity > self.stock:
            raise ValueError("Insufficient stock.")
        self.stock -= quantity

    def entity_mapping(prod) -> dict:
        res = {}
        prod_id = ''
        if prod is not None:
            if "_id" in prod:
                prod_id = str(prod["_id"])
            else:
                prod_id = prod["id"]
            res = {
                "id": prod_id,
                "name": prod["name"],
                "description": prod["description"],
                "price": prod["price"],
                "stock": prod["stock"],
                "category": prod["category"],
                "seller_id": prod["seller_id"]
            }
        return res

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "price": self.price.to_dict(),
            "stock": self.stock,
            "seller_id": self.seller_id,
            "category": self.category
        }