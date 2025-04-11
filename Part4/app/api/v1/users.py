from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model(
    'User', {
        'first_name': fields.String(
            required=True, description='First name of the user'),
        'last_name': fields.String(
            required=True, description='Last name of the user'),
        'password': fields.String(
            required=True, description='User\'s password'),
        'email': fields.String(
            required=True, description='Email of the user')
    }
)

user_update_model = api.model(
    'UserUpdate', {
        'first_name': fields.String(description='First name of the user'),
        'last_name': fields.String(description='Last name of the user'),
        'password': fields.String(description='User\'s password'),
        'email': fields.String(description='Email of the user')
    }
)


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        try:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400

            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'message': 'User successfully created'
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except TypeError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users"""
        users = facade.get_all_users()
        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
            for user in users
        ], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @api.doc(security="token")
    def get(self, user_id):
        """Get user details with ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.doc(security="token")
    @jwt_required()
    def put(self, user_id):
        """Update user details with ID"""
        user_data = api.payload
        current_user = get_jwt_identity()

        if current_user['id'] != user_id:
            return {'error': 'Unauthorized action'}, 403

        if 'email' in user_data or 'password' in user_data:
            return {'error': 'You cannot modify email or password.'}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)
            return {
                'id': updated_user.id,
                'message': 'User successfully updated',
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 404
        except TypeError as e:
            return {'error': str(e)}, 400
