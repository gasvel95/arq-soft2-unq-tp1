from pydantic import BaseModel, Field


class Price(BaseModel):
    amount: int = Field(ge=0)
    currency: str


    def to_dict(self):
        return {"amount": self.amount, "currency": self.currency}