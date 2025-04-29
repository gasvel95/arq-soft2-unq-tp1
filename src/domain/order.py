from typing import Optional
from bson import ObjectId
from pydantic import BaseModel
from domain.price import Price
from domain.product import Product


class Order(BaseModel):
    _id: Optional[ObjectId] = None
    id: Optional[str] = None
    buyer_id: str
    product_id: str
    quantity: int
    total: Optional[Price] = None
    

    def calculate_total(self,price: Price):
        self.total = Price(amount=price.amount * self.quantity, currency=price.currency)

    def to_dict(self):
        return {
            "buyer_id": self.buyer_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "total": self.total.to_dict()
        }