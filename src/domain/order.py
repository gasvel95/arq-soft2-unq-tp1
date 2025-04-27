from domain.product import Product


class Order:
    def __init__(self, id: str, buyer_id: str, product: Product, quantity: int):
        self.id = id
        self.buyer_id = buyer_id
        self.product_id = product.id
        self.quantity = quantity
        self.total = product.price.multiply(quantity)

    def to_dict(self):
        return {
            "id": self.id,
            "buyer_id": self.buyer_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "total": self.total.to_dict()
        }