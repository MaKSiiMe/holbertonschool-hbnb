#app/api/v1/users.py

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email')
})

@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.response(200, 'Users retrieved successfully')
    def get(self):
        """Retrieve all users (protected)"""
        users = facade.get_all_users()
        return [{'id': user['id'], 
                 'first_name': user['first_name'],
                 'last_name': user['last_name'],
                 'email': user['email']
                 } for user in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @jwt_required()
    @api.response(200, 'User retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Retrieve user details (protected)"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email}, 200
