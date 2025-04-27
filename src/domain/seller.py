class Seller:
    def __init__(self, id: str, company_name: str, email: str):
        self.id = id
        self.company_name = company_name
        self.email = email

    def to_dict(self):
        return {"id": self.id, "company_name": self.company_name, "email": self.email}