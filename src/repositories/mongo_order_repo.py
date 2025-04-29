from domain.order_repository_interface import OrderRepository
from domain.order import Order
from repositories.mongo_connect import db
from bson import ObjectId

class OrderRepositoryMongo(OrderRepository):
    def __init__(self):
        self.collection = db["orders"]

    def add(self, order: Order) -> Order:
        sale_data = order.to_dict()
        result = self.collection.insert_one(sale_data)
        order.id = str(result.inserted_id)
        return order

    def get(self, order_id: str) -> Order:
        data = self.collection.find_one({"_id": ObjectId(order_id)})
        if not data:
            raise Exception("Order not found")
        return Order(**data)

    def update(self, order: Order) -> Order:
        self.collection.update_one(
            {"_id": ObjectId(order.id)}, {"$set": order.to_dict()}
        )
        return order

    def delete(self, order_id: str) -> None:
        self.collection.delete_one({"_id": ObjectId(order_id)})
