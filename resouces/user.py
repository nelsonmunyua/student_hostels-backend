from flask_restful import Resource, reqparse
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models import User, db
from datetime import datetime
#from sqlalchemy.exc import IntegrityError


bcrypt = Bcrypt()


class Signup(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('first_name', required=True, help='First name is required')
    parser.add_argument('last_name', required=True, help='Last name is required')
    parser.add_argument('phone', required=True, help='Phone number is required')
    parser.add_argument('email', required=True, help='Email is required')
    parser.add_argument('password', required=True, help='Password is required')
    parser.add_argument('role', required=True, help='Role is required')

    def post(self):
        data = Signup.parser.parse_args()

        # Check email uniqueness
        if User.query.filter_by(email=data['email']).first():
            return {"message": "Email already taken", "status": "fail"}, 400

        # Check phone uniqueness
        if User.query.filter_by(phone=data['phone']).first():
            return {"message": "Phone number already taken", "status": "fail"}, 400

        

        try:
            # Hash password
            data['password'] = bcrypt.generate_password_hash(
            data['password']
            ).decode('utf-8')


            user = User(**data)
            db.session.add(user)
            db.session.commit()

            
            access_token = create_access_token(identity=user.id)

            return {
                "message": "Account created successfully",
                "status": "success",
                "user": user.to_dict(rules=('-password',)),
                "access_token": access_token
            }, 201

        except Exception as e:
            db.session.rollback()  
            return {
            "message": "Failed to create user",
            "error": str(e)
             }, 400
        

class Signin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, help='Email is required')
    parser.add_argument('password', required=True, help='Password is required')

    def post(self):
        data = Signin.parser.parse_args()

        user = User.query.filter_by(email=data['email']).first()

        if not user or not bcrypt.check_password_hash(
            user.password, data['password']
        ):
            return {
                "message": "Invalid email or password",
                "status": "fail"
            }, 401

        #  Tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        #  Login tracking
        user.last_login_at = datetime.utcnow()
        user.login_count += 1

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {
                "message": "Signin failed",
                "error": str(e)
            }, 400

        return {
            "message": "Signin successful",
            "status": "success",
            "user": user.to_dict(rules=('-password',)),
            "access_token": access_token,
            "refresh_token": refresh_token
        }, 200    

class RefreshToken(Resource):

    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()

        new_access_token = create_access_token(identity=user_id)

        return {
            "access_token": new_access_token
        }, 200        
