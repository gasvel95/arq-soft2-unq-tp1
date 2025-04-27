from domain.price import Price


class Product:
    def __init__(self, id: str, name: str, description: str, price: Price, stock: int, seller_id: str):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.seller_id = seller_id

    def reduce_stock(self, quantity: int):
        if quantity > self.stock:
            raise ValueError("Insufficient stock.")
        self.stock -= quantity

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price.to_dict(),
            "stock": self.stock,
            "seller_id": self.seller_id
        }