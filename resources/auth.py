from flask import request, current_app
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
import uuid

from models import db, User, Token
#from extensions import db
from utils.email import send_verification_email, send_password_reset_email

bcrypt = Bcrypt()


class Signup(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("first_name", required=True, help="First name required")
    parser.add_argument("last_name", required=True, help="Last name required")
    parser.add_argument("email", required=True, help="Email required")
    parser.add_argument("password", required=True, help="Password required")
    parser.add_argument("phone", required=True, help="Phone number required")
    parser.add_argument("role", default="student")

    def post(self):
        data = Signup.parser.parse_args()

        try:
            user = User(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                phone=data["phone"],
                role=data["role"],
                password_hash=bcrypt.generate_password_hash(
                    data["password"]
                ).decode("utf-8")
            )

            db.session.add(user)
            db.session.commit()

            # Email verification token
            token_value = str(uuid.uuid4())
            token = Token(
                user_id=user.id,
                token=token_value,
                token_type="email_verification",
                expires_at=datetime.utcnow() + timedelta(hours=24)
            )
            db.session.add(token)
            db.session.commit()

            # Try to send verification email, but don't fail if it errors
            try:
                send_verification_email(user, token_value)
            except Exception as email_error:
                # Log the error but don't fail signup
                print(f"Email sending failed: {email_error}")

            access_token = create_access_token(identity=user.id)

            return {
                "user": user.to_dict(),
                "token": access_token,
                "message": "Account created successfully"
            }, 201

        except IntegrityError as e:
            db.session.rollback()
            # Check which constraint was violated
            error_message = str(e).lower()
            if "ix_users_email" in error_message or "email" in error_message:
                return {"message": "Email already exists"}, 400
            elif "ix_users_phone" in error_message or "phone" in error_message:
                return {"message": "Phone number already exists"}, 400
            else:
                return {"message": "A user with this email or phone already exists"}, 400
        except Exception as e:
            db.session.rollback()
            return {"message": f"Signup failed: {str(e)}"}, 500
        

# login Api

class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("email", required=True, help="Email required")
    parser.add_argument("password", required=True, help="Password required")

    def post(self):
        data = Login.parser.parse_args()

        user = User.query.filter_by(email=data["email"]).first()

        if not user or not bcrypt.check_password_hash(
            user.password_hash, data["password"]
        ):
            return {"message": "Invalid email or password"}, 401

        access_token = create_access_token(identity=user.id, additional_claims={"role": user.role})
        refresh_token = create_refresh_token(identity=user.id)

        user.last_login_at = datetime.utcnow()
        user.login_count += 1
        db.session.commit()

        return {
            "user": user.to_dict(),
            "token": access_token,
            "refresh_token": refresh_token
        }, 200

class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)
        return {"token" : access_token}, 200
    
class Logout(Resource):
    @jwt_required(refresh=True)
    def post(self):
        try:
            # Get jwt token info
            jwt_data = get_jwt()
            jti = jwt_data["jti"]
            user_id = get_jwt_identity()

            revoked = Token(
                user_id=user_id,
                token=jti, 
                token_type="revoked",
                expires_at=datetime.utcnow()
            )

            db.session.add(revoked)
            db.session.commit()

            return {"message": "Logged out successfully. Token has been revoked."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Logout failed: {str(e)}"}, 500
        
class Me(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return {"message": "User not found"}, 404

        return {
            "user": user.to_dict(),
            "message": "User profile retrieved successfully"
            }, 200
    
class UpdateProfile(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("first_name")
    parser.add_argument("last_name")
    parser.add_argument("phone")

    @jwt_required()
    def put(self):
        user = User.query.get(get_jwt_identity())
        data = UpdateProfile.parser.parse_args()

        for field, value in data.items():
            if value:
                setattr(user, field, value)

        db.session.commit()
        return {"user": user.to_dict()}, 200
    
class ChangePassword(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("old_password", required=True)
    parser.add_argument("new_password", required=True)

    @jwt_required()
    def post(self):
        user = User.query.get(get_jwt_identity())
        data = ChangePassword.parser.parse_args()

        if not bcrypt.check_password_hash(
            user.password_hash, data["old_password"]
        ):
            return {"message": "Incorrect password"}, 400

        user.password_hash = bcrypt.generate_password_hash(
            data["new_password"]
        ).decode("utf-8")

        db.session.commit()
        return {"message": "Password changed successfully"}, 200


class VerifyEmail(Resource):
    # Parser for POST requests (JSON body)
    parser = reqparse.RequestParser()
    parser.add_argument("token", required=True, location="json")  # Specify location
    
    def get(self):
        """Handle GET requests from email verification links - redirect to frontend"""
        # Get token from query parameter
        token_value = request.args.get('token')
        
        if not token_value:
            from flask import redirect
            frontend_url = current_app.config.get("FRONTEND_URL", "http://localhost:5173")
            return redirect(f"{frontend_url}/login?error=verification_failed&message=Token is required")
            
        result = self._verify_token(token_value)
        
        # If verification was successful, redirect to login with success message
        if result[1] == 200:
            from flask import redirect
            frontend_url = current_app.config.get("FRONTEND_URL", "http://localhost:5173")
            return redirect(f"{frontend_url}/login?verified=true")
        
        # If verification failed, redirect to login with error
        error_message = result[0].get("message", "Verification failed")
        from flask import redirect
        frontend_url = current_app.config.get("FRONTEND_URL", "http://localhost:5173")
        return redirect(f"{frontend_url}/login?error=verification_failed&message={error_message}")
    
    def post(self):
        """Handle POST requests from API calls"""
        try:
            # Parse JSON body
            data = self.parser.parse_args()
            token_value = data["token"]
            
            return self._verify_token(token_value)
        except Exception as e:
            return {"message": f"Invalid request: {str(e)}"}, 400
    
    def _verify_token(self, token_value):
        """Common verification logic for both GET and POST"""
        token = Token.query.filter_by(
            token=token_value,
            token_type="email_verification"
        ).first()

        if not token or token.expires_at < datetime.utcnow():
            return {"message": "Invalid or expired token"}, 400

        user = User.query.get(token.user_id)
        if not user:
            return {"message": "User not found"}, 404
            
        user.is_verified = True
        db.session.delete(token)
        db.session.commit()

        return {
            "message": "Email verified successfully",
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "is_verified": user.is_verified
            }
        }, 200
    


class ForgotPassword(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("email", required=True)

    def post(self):
        email = ForgotPassword.parser.parse_args()["email"]
        user = User.query.filter_by(email=email).first()

        if user:
            token_value = str(uuid.uuid4())
            token = Token(
                user_id=user.id,
                token=token_value,
                token_type="password_reset",
                expires_at=datetime.utcnow() + timedelta(hours=1)
            )
            db.session.add(token)
            db.session.commit()

            send_password_reset_email(user, token_value)

        return {"message": "If email exists, reset link sent"}, 200
    
    
class ResetPassword(Resource):
    def get(self):
        """Handle GET requests - redirect to frontend with token"""
        token_value = request.args.get("token")
        frontend_url = current_app.config.get("FRONTEND_URL", "http://localhost:5173")
        
        if not token_value:
            # Redirect to frontend with error
            from flask import redirect
            return redirect(f"{frontend_url}/reset-password?error=token_required")
        
        # Check token validity
        token = Token.query.filter_by(
            token=token_value,
            token_type="password_reset"
        ).first()
        
        if not token:
            # Redirect to frontend with error
            from flask import redirect
            return redirect(f"{frontend_url}/reset-password?error=invalid_token")
        
        if token.expires_at < datetime.utcnow():
            # Delete expired token
            db.session.delete(token)
            db.session.commit()
            # Redirect to frontend with error
            from flask import redirect
            return redirect(f"{frontend_url}/reset-password?error=expired_token")
        
        # Token is valid - redirect to frontend with token
        from flask import redirect
        return redirect(f"{frontend_url}/reset-password?token={token_value}")
    
    def post(self):
        """Actually reset password"""
        if not request.is_json:
            return {"message": "Content-Type must be application/json"}, 415
        
        data = request.get_json()
        token_value = data.get("token")
        password = data.get("password")
        
        if not token_value or not password:
            return {"message": "Token and password are required"}, 400
        
        # Check token
        token = Token.query.filter_by(
            token=token_value,
            token_type="password_reset"
        ).first()
        
        if not token:
            return {"message": "Invalid token"}, 400
        
        if token.expires_at < datetime.utcnow():
            return {"message": "Token has expired"}, 400
        
        # Update password
        user = User.query.get(token.user_id)
        user.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        
        # Delete token
        db.session.delete(token)
        db.session.commit()
        
        return {"message": "Password reset successful"}, 200
