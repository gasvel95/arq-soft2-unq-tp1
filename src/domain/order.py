from typing import Optional
from bson import ObjectId
from pydantic import BaseModel
from domain.price import Price


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
    def entity_mapping(ord) -> dict:
        res = {}
        ord_id = ''
        if ord is not None:
            if "_id" in ord:
                ord_id = str(ord["_id"])
            else:
                ord_id = ord["id"]
            res = {
                "id": ord_id,
                "buyer_id": ord["buyer_id"],
                "product_id": ord["product_id"],
                "quantity": ord["quantity"],
                "total": ord["total"]
            }
        return res