import uuid
from domain.user import User
from domain.user_repository_interface import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository): self.user_repo = user_repo
    def create_user(self, first_name: str, last_name: str, email: str) -> User:
        user = User(str(uuid.uuid4()), first_name, last_name, email)
        self.user_repo.add(user)
        return user
    def get_user(self, id: str) -> User:
        u = self.user_repo.get(id)
        if u is None: raise ValueError("User not found")
        return u