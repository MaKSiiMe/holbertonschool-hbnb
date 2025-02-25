from BaseModel import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        if not first_name:
            raise ValueError("first_name must not be emplty")
        if not last_name:
            raise ValueError("last_name must not be emplty")
        if not email:
            raise ValueError("email must not be emplty")
        
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []

    def update_password(self, password):
        self.password = password
        self.save()
    
    def add_place(self, place):
        self.places.append(place)