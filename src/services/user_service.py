import uuid

from bson import ObjectId
from domain.price import Price
from domain.user import User
from domain.user_repository_interface import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository): self.user_repo = user_repo
    def create_user(self, usr:User) -> User:
        return self.user_repo.add(usr)
    def get_user(self, id: str) -> User:
        try:
            return self.user_repo.get(id)
        except: 
            raise ValueError("User not found")
    def update_user(self,id: str, usr: User) -> User:
        usr.id = id
        self.user_repo.update(usr)
        return usr
    def delete_user(self,id:str):
        return self.user_repo.delete(id)
    def discount_amount(self,id:str,amount:Price):
        try:
            user = User(**self.user_repo.get(id))
            user.discount_wallet(amount)
            self.user_repo.update(user)
            return user
        except: 
            raise ValueError("User not found")
    def charge_amount(self,id:str,amount:Price):
        try:
            user= User(**self.user_repo.get(id))
            user.charge_wallet(amount)
            self.user_repo.update(user)
            return user
        except: 
            raise ValueError("User not found")