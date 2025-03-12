from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description="User first name", example="John"),
    'last_name': fields.String(required=True, description="User last name", example="Doe"),
    'email': fields.String(required=True, description="User email", example="john@email.com"),
    'password': fields.String(required=True, description="User password", example="Johnd0e!")
})

user_update_model = api.model('User Update', {
    'first_name': fields.String(description='First name of the user', example="Jane"),
    'last_name': fields.String(description='Last name of the user', example="Doe"),
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # if "is_admin" in user_data:
        #     api.abort(400, 'Invalid input data')

        try:
            new_user = facade.create_user(user_data)
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return new_user.to_dict(), 201
    
    @api.response(200, "Users retrieved successfully")
    def get(self):
        """Retrieve a list of all users"""
        all_users = facade.get_all_users()
        return [user.to_dict() for user in all_users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        return user.to_dict(), 200

    @api.expect(user_update_model)
    @api.response(201, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, user_id):
        """Update a user"""
        current_user = get_jwt_identity()

        if not facade.get_user(user_id):
            api.abort(404, 'User not found')

        """Get user details by ID"""
        user = facade.get_user(current_user.get('id'))
        if user_id != user.id:
            api.abort(403, "Unauthorized action")

        user_data = api.payload
        
        valid_inputs = ["first_name", "last_name"]
        for key in user_data:
            if key not in valid_inputs:
                api.abort(400, f'Invalid input data: {key}')

        try:
            user.update(user_data)
            updated_user = facade.update_user(user_id, user.to_dict())
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return updated_user.to_dict(), 201