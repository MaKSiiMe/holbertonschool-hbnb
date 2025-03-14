from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.extensions import db, bcrypt, jwt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

# Defining login_model before using it
login_model = api.model('Login', {
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
        except Exception as e:
            return {'error': str(e)}, 400
        except ValueError:
            return {'error': 'Invalid input data'}, 400
        
    @jwt_required()
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
    @jwt_required()
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
    
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(200, 'User sucessfully updated')
    @api.response(404, 'User not found')
    @api.response(403, 'Forbidden')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user details by ID"""
        user_data = api.payload
        current_user_id = get_jwt_identity()['id']
        
        # Authorization verification
        if user_id != current_user_id:
            return {'error': 'You are not authorized to update this user'}, 403
        # Data validation
        if 'email' in user_data or 'password' in user_data:
            return {'error': 'Email and password cannot be updated here'}, 400

        """Check if the user exists"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
       
        updated_user = facade.update_user(user_id, user_data)
        return {'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email}, 200

@api.route('/login')
class LoginResource(Resource):
    @api.doc(description="User login")
    @api.expect(login_model)
    def post(self):
        data = api.payload
        user = facade.get_user_by_email(data['email'])
        if user and bcrypt.check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity={'id': user.id, 'is_admin':user.is_admin})
            return {'access_token': access_token}, 200
        else:
            return {'error': 'Invalid credentials'}, 401
