from typing import Optional
from bson import ObjectId
from pydantic import BaseModel


class Seller(BaseModel):
    _id: Optional[ObjectId] = None
    id: Optional[str] = None
    company_name: str
    email: str

    def to_dict(self):
        return { "company_name": self.company_name, "email": self.email}
    
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
                "email": seller["email"]
            }
        return res