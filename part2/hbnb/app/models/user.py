from basemodel import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.password = None

    def add_user(self, user):
        self.user.append(user)
        self.save()
    
    def get_user(self, user_id):
        for user in self.user:
            if user.id == user_id:
                return user
        return None
    
    def get_user_by_email(self, email):
        for user in self.user:
            if user.email == email:
                return user
        return None
    