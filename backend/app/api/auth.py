from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..models.user import User
from .. import db
import logging

# Create auth blueprint
auth_bp = Blueprint('auth', __name__)

# Configure logger
logger = logging.getLogger(__name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['email', 'username', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 400
    
    # Create new user
    user = User(
        email=data['email'],
        username=data['username'],
        password=data['password'],
        is_admin=data.get('is_admin', False)
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Generate access token - ensure identity is a string
    user_id_str = str(user.id)
    logger.info(f"Creating token for user ID: {user_id_str} (type: {type(user_id_str)})")
    access_token = create_access_token(identity=user_id_str)
    
    return jsonify({
        'message': 'User registered successfully',
        'user': user.to_dict(),
        'access_token': access_token
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login a user."""
    try:
        logger.info("Login attempt received")
        data = request.get_json()
        logger.info(f"Login data: {data}")
        
        # Validate required fields
        if 'email' not in data or 'password' not in data:
            logger.warning("Missing email or password in login request")
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user by email
        user = User.query.filter_by(email=data['email']).first()
        
        if not user:
            logger.warning(f"Login failed: User not found with email {data['email']}")
            return jsonify({'error': 'Invalid email or password'}), 401
        
        logger.info(f"User found: {user.username}, ID: {user.id}, Admin: {user.is_admin}")
        logger.info(f"User created_at: {user.created_at}, updated_at: {user.updated_at}")
        
        # Check password
        if not user.check_password(data['password']):
            logger.warning(f"Login failed: Invalid password for user {user.email}")
            return jsonify({'error': 'Invalid email or password'}), 401
        
        logger.info(f"Password verified for user {user.email}")
        
        # Generate access token - ensure identity is a string
        user_id_str = str(user.id)
        logger.info(f"Creating token for user ID: {user_id_str} (type: {type(user_id_str)})")
        access_token = create_access_token(identity=user_id_str)
        
        # Create user dict with safe handling of datetime fields
        user_dict = user.to_dict()
        logger.info(f"User dict created: {user_dict}")
        
        return jsonify({
            'message': 'Login successful',
            'user': user_dict,
            'access_token': access_token
        }), 200
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get the current authenticated user."""
    user_id = get_jwt_identity()
    logger.info(f"JWT identity: {user_id} (type: {type(user_id)})")
    
    # Convert to int if the identity is a string (which it should be)
    if isinstance(user_id, str) and user_id.isdigit():
        user_id = int(user_id)
    
    user = User.query.get(user_id)
    
    if not user:
        logger.warning(f"User not found with ID: {user_id}")
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200


@auth_bp.route('/validate-token', methods=['GET'])
@jwt_required()
def validate_token():
    """Validate the JWT token and return user details."""
    try:
        user_id = get_jwt_identity()
        logger.info(f"Validating token with identity: {user_id} (type: {type(user_id)})")
        
        # Convert to int if the identity is a string (which it should be)
        if isinstance(user_id, str) and user_id.isdigit():
            user_id = int(user_id)
        
        user = User.query.get(user_id)
        
        if not user:
            logger.warning(f"Token validation failed: User not found with ID {user_id}")
            return jsonify({'valid': False, 'error': 'User not found'}), 404
            
        logger.info(f"Token validation successful for user: {user.username}")
        return jsonify({
            'valid': True,
            'user': user.to_dict()
        }), 200
    except Exception as e:
        logger.error(f"Token validation error: {str(e)}")
        return jsonify({'valid': False, 'error': str(e)}), 401


@auth_bp.route('/test', methods=['GET'])
def test_api():
    """Test endpoint that doesn't require authentication."""
    return jsonify({
        'message': 'API is working correctly',
        'status': 'success'
    }), 200 