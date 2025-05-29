from typing import Optional
from bson import ObjectId
from pydantic import BaseModel

from domain.price import Price


class User(BaseModel):
    _id: Optional[ObjectId] = None
    id: Optional[str] = None
    first_name: str
    last_name: str
    email: str
    wallet: int = 0

    def list_serial_user(users) -> list:
        return [User.user_entity(user) for user in users]

    def to_dict(self):
        return { "first_name": self.first_name, "last_name": self.last_name, "email": self.email, "wallet": self.wallet}
    
    def entity_mapping(usr) -> dict:
        res = {}
        usr_id = ''
        if usr is not None:
            if "_id" in usr:
                usr_id = str(usr["_id"])
            else:
                usr_id = usr["id"]
            res = {
                "id": usr_id,
                "first_name": usr["first_name"],
                "last_name": usr["last_name"],
                "email": usr["email"],
                "wallet": usr["wallet"]
            }
        return res
    
    def charge_wallet(self,price:Price):
        self.wallet += price.amount

    def discount_wallet(self,price:Price):
        self.wallet -= price.amount   