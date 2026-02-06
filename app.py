from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from config import Config
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
import os

# Load environment variables
load_dotenv(override=True)

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes with proper configuration
CORS(app, 
    resources={r"/api/*": {"origins": ["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174"]}},
    supports_credentials=True,
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"]
)

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
from resources.auth import Signup, Login, RefreshToken, Logout, VerifyEmail, Me, UpdateProfile, ChangePassword, ForgotPassword, ResetPassword

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

# Student dashboard stats endpoint
@app.route('/student/dashboard-stats', methods=['GET'])
@cross_origin(supports_credentials=True)
def student_dashboard_stats():
    """Get student dashboard statistics"""
    return {
        "stats": {
            "totalBookings": 0,
            "activeBookings": 0,
            "wishlistCount": 0,
            "reviewsGiven": 0
        },
        "recentBookings": []
    }, 200



