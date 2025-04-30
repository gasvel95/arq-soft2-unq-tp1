import uuid

from bson import ObjectId
from domain.user import User
from domain.user_repository_interface import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository): self.user_repo = user_repo
    def create_user(self, usr:User) -> User:
        return self.user_repo.add(usr)
    def get_user(self, id: str) -> User:
        u = self.user_repo.get(id)
        if u is None: raise ValueError("User not found")
        return u
    def update_user(self,id: str, usr: User) -> User:
        usr.id = id
        self.user_repo.update(usr)
        return usr