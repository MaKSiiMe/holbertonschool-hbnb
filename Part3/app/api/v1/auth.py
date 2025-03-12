#app/api/v1/auth.py

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth', description='User authentication')

auth_model = api.model('Auth', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class AuthLogin(Resource):
    @api.expect(auth_model, validate=True)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return JWT token"""
        auth_data = api.payload
        user = facade.get_user_by_email(auth_data['email'])

        if not user or not user.verify_password(auth_data['password']):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200
