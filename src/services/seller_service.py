import uuid
from domain.price import Price
from domain.seller import Seller
from domain.seller_repository_interface import SellerRepository


class SellerService:
    def __init__(self, seller_repo: SellerRepository): self.seller_repo = seller_repo
    def create_seller(self, seller: Seller) -> Seller:
        return self.seller_repo.add(seller)
    def update_seller(self, seller_id: str, seller: Seller) -> Seller:
        seller.id = seller_id
        self.seller_repo.update(seller)
        return seller
    def get_seller(self, id: str) -> Seller:
        try:
            return self.seller_repo.get(id)
        except:
            raise ValueError("Seller not found")
    def delete_seller(self,id:str):
        return self.seller_repo.delete(id)
    
    def discount_amount(self,id:str,amount:Price):
        try:
            seller = Seller(**self.seller_repo.get(id))
            seller.discount_wallet(amount)
            self.seller_repo.update(seller)
            return seller
        except: 
            raise ValueError("seller not found")
    def charge_amount(self,id:str,amount:Price):
        try:
            seller = Seller(**self.seller_repo.get(id))
            seller.charge_wallet(amount)
            self.seller_repo.update(seller)
            return seller
        except: 
            raise ValueError("seller not found")