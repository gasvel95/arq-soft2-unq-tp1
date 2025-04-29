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