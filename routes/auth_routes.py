from flask import Blueprint,request,jsonify
from extensions import db
from models.user import User
from flask_jwt_extended import create_access_token
auth_bp=Blueprint('auth',__name__)

@auth_bp.route('/signup',methods=['POST'])
def signup():
    """
    User Registration
    Create a new account by providing a username, email, and password.
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - email
            - password
          properties:
            username:
              type: string
              example: "new_developer"
            email:
              type: string
              example: "dev@example.com"
            password:
              type: string
              example: "securepassword123"
    responses:
      201:
        description: User created successfully
      400:
        description: Registration failed (e.g., username/email already exists)
    """
    data=request.get_json()
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({"Error":"Email already registered"}),400
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({"Error":"Username already taken"}),400
    new_user=User(
        username=data.get('username'),
        email=data.get('email')
    )
    new_user.set_password(data.get('password'))

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully!"}), 201
@auth_bp.route('/login',methods=['POST'])
def login():
    """
    User Login
    Authenticate with email and password to receive a JWT token.
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: "dev@example.com"
            password:
              type: string
              example: "securepassword123"
    responses:
      200:
        description: Returns the JWT access token
      401:
        description: Invalid credentials
    """
    data=request.get_json()

    user=User.query.filter_by(email=data.get('email')).first()
    if user and user.check_password(data.get('password')):
        access_token=create_access_token(identity=str(user.id))
        return jsonify({"message":f"Welcome back,{user.username}!",
                       "token":access_token 
                       }),200
    else:
        return jsonify({"Error": "Invalid email or password"}),401
    
    