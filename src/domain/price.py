class Price:
    def __init__(self, amount: float, currency: str = "USD"):
        if amount < 0:
            raise ValueError("Amount must be non-negative.")
        self.amount = amount
        self.currency = currency

    def multiply(self, factor: int) -> 'Price':
        return Price(self.amount * factor, self.currency)

    def to_dict(self):
        return {"amount": self.amount, "currency": self.currency}