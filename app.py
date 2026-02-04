from flask import Flask
from flask_migrate import Migrate
from models import db
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from config import Config
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(override=True)

# Initialize Flask app
app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///student_hostel.db"
app.config["SQLALCHEMY_ECHO"] = True
app.config["BUNDLE_ERRORS"] = True

# JWT Configuration
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "jwt-super-secret")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 900        # 15 minutes
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 86400 * 7 # 7 days

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)

# Import resources
from resouces.auth import Signup, Login, RefreshToken, Logout, VerifyEmail, Me, UpdateProfile, ChangePassword, ForgotPassword, ResetPassword

@app.route('/')
def index():
    return {"Message": "Student-hostel server running"}

# Add routes
api.add_resource(Signup, '/auth/signup')
api.add_resource(Login, '/auth/login')
api.add_resource(Logout, '/auth/logout')
api.add_resource(RefreshToken, '/auth/refresh')
api.add_resource(Me, "/auth/me")
api.add_resource(UpdateProfile, "/auth/profile")
api.add_resource(ChangePassword, "/auth/change-password")
api.add_resource(VerifyEmail, "/auth/verify-email")
api.add_resource(ForgotPassword, "/auth/forgot-password", endpoint="forgotpassword")
api.add_resource(ResetPassword, "/auth/reset-password", endpoint="resetpassword")

@app.route('/test-email')
def test_email():
    """Test endpoint to verify email configuration"""
    from flask_mail import Message
    try:
        msg = Message(
            subject="Test Email from Student Hostel App",
            recipients=["nelsonmunyua8@gmail.com"],
            html="<h1>Email Test Successful!</h1><p>Your Brevo SMTP is working correctly.</p>"
        )
        mail.send(msg)
        return {
            "success": True,
            "message": "Test email sent successfully!",
            "config": {
                "mail_server": app.config.get("MAIL_SERVER"),
                "mail_username": app.config.get("MAIL_USERNAME"),
                "mail_sender": app.config.get("MAIL_DEFAULT_SENDER")
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "config": {
                "mail_server": app.config.get("MAIL_SERVER"),
                "mail_username": app.config.get("MAIL_USERNAME"),
                "mail_port": app.config.get("MAIL_PORT")
            }
        }, 500

if __name__ == "__main__":
    # Debug info
    print("=" * 50)
    print("EMAIL CONFIGURATION CHECK:")
    print(f"MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
    print(f"MAIL_PORT: {app.config.get('MAIL_PORT')}")
    print(f"MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
    print(f"MAIL_DEFAULT_SENDER: {app.config.get('MAIL_DEFAULT_SENDER')}")
    print(f"MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
    print(f"MAIL_USE_SSL: {app.config.get('MAIL_USE_SSL')}")
    print("=" * 50)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    app.run(port=5000, debug=True)