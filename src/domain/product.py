from typing import Optional
from bson import ObjectId
from pydantic import BaseModel
from domain.price import Price


class Product(BaseModel):
    _id: Optional[ObjectId] = None
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    price: Price
    stock: int
    seller_id: str


    def reduce_stock(self, quantity: int):
        if quantity > self.stock:
            raise ValueError("Insufficient stock.")
        self.stock -= quantity

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "price": self.price.to_dict(),
            "stock": self.stock,
            "seller_id": self.seller_id
        }