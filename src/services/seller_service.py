import uuid
from domain.seller import Seller
from domain.seller_repository_interface import SellerRepository


class SellerService:
    def __init__(self, seller_repo: SellerRepository): self.seller_repo = seller_repo
    def create_seller(self, company_name: str, email: str) -> Seller:
        s = Seller(str(uuid.uuid4()), company_name, email)
        self.seller_repo.add(s)
        return s
    def get_seller(self, id: str) -> Seller:
        s = self.seller_repo.get(id)
        if s is None: raise ValueError("Seller not found")
        return s