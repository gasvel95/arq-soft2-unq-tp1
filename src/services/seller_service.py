import uuid
from domain.seller import Seller
from domain.seller_repository_interface import SellerRepository


class SellerService:
    def __init__(self, seller_repo: SellerRepository): self.seller_repo = seller_repo
    def create_seller(self, seller: Seller) -> str:
        return self.seller_repo.add(seller)
    def update_seller(self, seller_id: str, seller: Seller) -> Seller:
        seller._id = seller_id
        self.seller_repo.update(seller)
        return seller
    def get_seller(self, id: str) -> Seller:
        s = self.seller_repo.get(id)
        if s is None: raise ValueError("Seller not found")
        return s