from flask_restx import Namespace, Resource
from app.services.facade import facade

api = Namespace('users', description="User operations")

@api.route('/')
class UserList(Resource):
    def get(self):
        """Fetch all users"""
        return [user.to_dict() for user in facade.user_repo.get_all()]
