from domain.seller_repository_interface import SellerRepository
from domain.seller import Seller
from repositories.mongo_connect import db
from bson import ObjectId

class SellerRepositoryMongo(SellerRepository):
    def __init__(self):
        self.collection = db["sellers"]

    def add(self, seller: Seller) -> str:
        seller_data = seller.to_dict()
        result = self.collection.insert_one(seller_data)
        return str(result.inserted_id)

    def get(self, seller_id: str) -> Seller:
        data = self.collection.find_one({"_id": ObjectId(seller_id)})
        if not data:
            raise Exception("Seller not found")
        return Seller(**data)

    def update(self, seller: Seller) -> Seller:
        self.collection.update_one(
            {"_id": ObjectId(seller.id)}, {"$set": seller.to_dict()}
        )
        return seller

    def delete(self, seller_id: str) -> None:
        self.collection.delete_one({"_id": ObjectId(seller_id)})
