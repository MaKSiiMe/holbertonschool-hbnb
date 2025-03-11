from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.extensions import bcrypt


api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        #Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        
        try:
            #Validate password strength
            if len(user_data['password']) < 8:
                return {'error': 'Password must be at least 8 characters long'}, 400
            
            """ Hash the password before creating the user"""
            user_data['password'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')

            """ Create a new user"""
            new_user = facade.create_user(user_data)
            return {'id': new_user.id, 'message': 'User successfully created'}, 201
        except facade.UserCreationError as e:
            return {'error': str(e)}, 400
        except ValueError:
            return {'error': 'Invalid input data'}, 400
        
    
    @api.response(200, 'User details retrieved successfully')
    def get(self):
        users = facade.get_all_users()
        return [{'id': user['id'], 
                 'first_name': user['first_name'],
                 'last_name': user['last_name'],
                 'email': user['email']
                 } for user in users], 200
    
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email}, 200
    
    @api.expect(user_model, validate=True)
    @api.response(200, 'User sucessfully updated')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user details by ID"""
        user_data = api.payload
        
        """Check if the user exists"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Check if the email is already registered by another user
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user and existing_user.id != user.id:
            return {'error': 'Email already registered by another user'}, 400
        
        updated_user = facade.update_user(user_id, user_data)
        return {'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email}, 200
