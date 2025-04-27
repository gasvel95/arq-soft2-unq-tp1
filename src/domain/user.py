class User:
    def __init__(self, id: str, first_name: str, last_name: str, email: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def to_dict(self):
        return {"id": self.id, "first_name": self.first_name, "last_name": self.last_name, "email": self.email}