from typing import Optional
from bson import ObjectId
from pydantic import BaseModel

from domain.price import Price


class Seller(BaseModel):
    _id: Optional[ObjectId] = None
    id: Optional[str] = None
    company_name: str
    email: str
    wallet: int = 0

    def to_dict(self):
        return { "company_name": self.company_name, "email": self.email, "wallet": self.wallet}
    
    def entity_mapping(seller) -> dict:
        res = {}
        seller_id = ''
        if seller is not None:
            if "_id" in seller:
                seller_id = str(seller["_id"])
            else:
                seller_id = seller["id"]
            res = {
                "id": seller_id,
                "company_name": seller["company_name"],
                "email": seller["email"],
                "wallet": seller["wallet"]
            }
        return res
    
    def charge_wallet(self,price:Price):
        self.wallet += price.amount

    def discount_wallet(self,price:Price):
        self.wallet -= price.amount   