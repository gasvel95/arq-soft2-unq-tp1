from typing import Optional
from bson import ObjectId
from pydantic import BaseModel


class User(BaseModel):
    _id: Optional[ObjectId] = None
    id: Optional[str] = None
    first_name: str
    last_name: str
    email: str

    def list_serial_user(users) -> list:
        return [User.user_entity(user) for user in users]

    def to_dict(self):
        return { "first_name": self.first_name, "last_name": self.last_name, "email": self.email}