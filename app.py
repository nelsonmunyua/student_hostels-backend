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
from seed import seed_database
import os
# Load environment variables
load_dotenv(override=True)

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes with proper configuration
#CORS(app)
CORS(app, 
    resources={r"/*": {"origins": ["http://localhost:5173", "https://student-hostels-frontend-3d23.vercel.app", "https://*.vercel.app"]}},
    supports_credentials=True,
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"]
)

# Load configuration
app.config.from_object(Config)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_ECHO"] = True
app.config["BUNDLE_ERRORS"] = True

# JWT Configuration
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "jwt-super-secret")
app.config["JWT_ALGORITHM"] = "HS256"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 900        # 15 minutes
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 86400 * 7 # 7 days

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)

from resources.auth import (
    Signup, Login, RefreshToken, Logout, VerifyEmail, 
    Me, UpdateProfile, ChangePassword, ForgotPassword, ResetPassword
)

from resources.admin.admin import ( AdminDashboardResource, AdminUsersResource, AdminUserStatusResource, AdminAnalyticsResource,
AdminHostelsResource, AdminHostVerificationAction, AdminBookingsResource, AdminSettingsResource, AdminHostVerificationResource,
AdminHostelStatusResource, AdminPaymentResource, AdminPaymentStatusResourse, AdminReviewDeleteResource, AdminReviewResource 
)




@app.route('/')
def index():
    return {"Message": "Student-hostel server running"}
 # Authentication Routes
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

 # Admin Routes
api.add_resource(AdminDashboardResource, "/admin/dashboard") 
api.add_resource(AdminUsersResource, "/admin/users")
api.add_resource(AdminUserStatusResource, "/admin/users/<int:user_id>")
api.add_resource(AdminHostelsResource, "/admin/hostels")
api.add_resource(AdminHostelStatusResource, "/admin/hostels/<int:hostel_id>")

api.add_resource(AdminBookingsResource, "/admin/bookings")

api.add_resource(AdminPaymentResource, "/admin/payments")
api.add_resource(AdminPaymentStatusResourse, "/admin/payments/<int:payment_id>")

api.add_resource(AdminReviewResource, "/admin/reviews")
api.add_resource(AdminReviewDeleteResource, "/admin/reviews/<int:review_id>")

api.add_resource(AdminHostVerificationResource, "/admin/verifications")
api.add_resource(AdminHostVerificationAction, "/admin/verifications/<int:verification_id>")

api.add_resource(AdminAnalyticsResource, "/admin/analytics")
api.add_resource(AdminSettingsResource, "/admin/settings")


@app.cli.command("seed")
def seed_command():
    """Seed the database with sample data"""
    with app.app_context():
        seed_database()
    print("Database seeded!")

if __name__ == "__main__":
    app.run(debug=True)

