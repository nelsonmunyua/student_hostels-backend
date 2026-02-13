from flask import Flask, jsonify, make_response
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
from jwt.exceptions import ExpiredSignatureError as JWTExpiredError
from jwt.exceptions import InvalidTokenError
import os
# Load environment variables
load_dotenv(override=True)

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes with proper configuration
# Allow all origins in development
allowed_origins = [
    "http://localhost:5173",  # local dev
    "https://student-hostels-frontend-3d23.vercel.app",  # your deployed frontend
    "*"  # Allow all origins in development
]

CORS(
    app,
    resources={r"/*": {"origins": allowed_origins}},
    supports_credentials=True,
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
    expose_headers=["Content-Type", "Authorization"],
    max_age=86400
)

# Load configuration
app.config.from_object(Config)

# Get database URL with SSL mode
database_url = Config.get_database_url()
if not database_url:
    raise RuntimeError("DATABASE_URL is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url

# Connection pool settings for stability on Render
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,  # Verify connections before using
    "pool_recycle": 300,    # Recycle connections every 5 minutes
    "pool_size": 5,         # Base pool size
    "max_overflow": 10,      # Allow up to 10 additional connections
    "pool_timeout": 30,       # Timeout for getting connection from pool
}

app.config["SQLALCHEMY_ECHO"] = False  # Disable echo in production to reduce log noise
app.config["BUNDLE_ERRORS"] = True


# Handle OPTIONS requests for preflight CORS
@app.route('/auth/signup', methods=['OPTIONS'])
@app.route('/auth/login', methods=['OPTIONS'])
@app.route('/auth/logout', methods=['OPTIONS'])
@app.route('/auth/refresh', methods=['OPTIONS'])
@app.route('/auth/me', methods=['OPTIONS'])
@app.route('/auth/profile', methods=['OPTIONS'])
@app.route('/auth/change-password', methods=['OPTIONS'])
@app.route('/auth/verify-email', methods=['OPTIONS'])
@app.route('/auth/forgot-password', methods=['OPTIONS'])
@app.route('/auth/reset-password', methods=['OPTIONS'])
@app.route('/host/dashboard', methods=['OPTIONS'])
@app.route('/host/availability', methods=['OPTIONS'])
@app.route('/bookings', methods=['OPTIONS'])
@app.route('/payments/initialize', methods=['OPTIONS'])
@app.route('/payments/mpesa', methods=['OPTIONS'])
@app.route('/payments/card', methods=['OPTIONS'])
def handle_cors_options():
    """Handle OPTIONS preflight requests for CORS"""
    response = make_response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    response.headers['Access-Control-Max-Age'] = '86400'
    return response

# JWT Configuration
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "jwt-super-secret")
app.config["JWT_ALGORITHM"] = "HS256"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 86400 * 7      # 7 days (was 8 hours)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 86400 * 30 # 30 days (was 7 days)

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

from resources.host import (
    HostDashboard,
    HostProfile,
    HostListings,
    HostListingDetail,
    HostRooms,
    HostRoomDetail,
    HostBookings,
    HostBookingDetail,
    HostEarnings,
    HostReviews,
    HostNotifications,
    HostNotificationDetail,
    HostVerificationResource,
    HostSupport,
    HostSupportTickets,
    HostAnalytics,
    HostAvailability,
    HostHostelAvailability,
    HostRoomAvailabilityUpdate,
    HostAvailabilityCalendar
)

from resources.admin.admin import ( 
    AdminDashboardResource,
    AdminUsersResource, 
    AdminUserStatusResource, 
    AdminAnalyticsResource,
    AdminHostelsResource, 
    AdminHostVerificationAction, 
    AdminBookingsResource, 
    AdminBookingDetailResource,
    AdminSettingsResource, 
    AdminHostVerificationResource,
    AdminHostelStatusResource, 
    AdminPaymentResource, 
    AdminPaymentStatusResourse, 
    AdminReviewDeleteResource, 
    AdminReviewResource,
    AdminReviewStatusResource,
    AdminSupportTicketsResource,
    AdminSupportTicketDetailResource
)

from resources.student import (
    StudentAccommodations,
    StudentAccommodationDetail,
    StudentWishlist,
    StudentWishlistItem,
    StudentWishlistCheck,
    StudentReviews,
    StudentReviewDetail,
    StudentPendingReviews,
    StudentPayments,
    StudentPaymentStats,
    StudentNotifications,
    StudentNotificationDetail,
    StudentSupport,
    StudentSupportTickets,
    StudentDashboardStats,
    StudentBookings,
    StudentBookingDetail
)

from resources.payment import (
    PaymentResource,
    MpesaPaymentResource,
    MpesaStatusResource,
    CardPaymentResource,
    StripePaymentResource,
    PaymentDetailResource,
    PaymentByBookingResource,
    PaymentStatsResource,
    MpesaCallbackResource
)

from resources.booking import (
    BookingResource,
    BookingDetailResource,
    BookingAvailabilityResource,
    BookingCancelResource
)


#postgresql://root:VcUrgCvgV0Qx4Y73mWH1aDbOhFUctzsD@dpg-d63mr9shg0os73ckn7o0-a.virginia-postgres.render.com/student_hostel_xopf


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
api.add_resource(AdminBookingDetailResource, "/admin/bookings/<int:booking_id>")

api.add_resource(AdminPaymentResource, "/admin/payments")
api.add_resource(AdminPaymentStatusResourse, "/admin/payments/<int:payment_id>")

api.add_resource(AdminReviewResource, "/admin/reviews")
api.add_resource(AdminReviewStatusResource, "/admin/reviews/<int:review_id>/status")
api.add_resource(AdminReviewDeleteResource, "/admin/reviews/<int:review_id>")

api.add_resource(AdminHostVerificationResource, "/admin/verifications")
api.add_resource(AdminHostVerificationAction, "/admin/verifications/<int:verification_id>")

api.add_resource(AdminAnalyticsResource, "/admin/analytics")
api.add_resource(AdminSettingsResource, "/admin/settings")

# Admin Support Ticket Routes
api.add_resource(AdminSupportTicketsResource, "/admin/support/tickets")
api.add_resource(AdminSupportTicketDetailResource, "/admin/support/tickets/<int:ticket_id>")

# Student Routes
api.add_resource(StudentAccommodations, "/student/accommodations")
api.add_resource(StudentAccommodationDetail, "/student/accommodations/<int:hostel_id>")
api.add_resource(StudentWishlist, "/student/wishlist")
api.add_resource(StudentWishlistItem, "/student/wishlist/<int:hostel_id>")
api.add_resource(StudentWishlistCheck, "/student/wishlist/check/<int:hostel_id>")
api.add_resource(StudentReviews, "/student/reviews")
api.add_resource(StudentReviewDetail, "/student/reviews/<int:review_id>")
api.add_resource(StudentPendingReviews, "/student/reviews/pending")
api.add_resource(StudentPayments, "/student/payments")
api.add_resource(StudentPaymentStats, "/student/payments/stats")
api.add_resource(StudentNotifications, "/student/notifications")
api.add_resource(StudentNotificationDetail, "/student/notifications/<int:notification_id>")
api.add_resource(StudentSupport, "/student/support")
api.add_resource(StudentSupportTickets, "/student/support/tickets")
api.add_resource(StudentDashboardStats, "/student/dashboard-stats")
api.add_resource(StudentBookings, "/student/bookings")
api.add_resource(StudentBookingDetail, "/student/bookings/<int:booking_id>")

# Payment Routes
api.add_resource(PaymentResource, "/payments/initialize")
api.add_resource(MpesaPaymentResource, "/payments/mpesa")
api.add_resource(MpesaStatusResource, "/payments/mpesa/status/<checkout_request_id>")
api.add_resource(CardPaymentResource, "/payments/card")
api.add_resource(StripePaymentResource, "/payments/stripe/<action>")
api.add_resource(PaymentDetailResource, "/payments/<int:payment_id>")
api.add_resource(PaymentByBookingResource, "/payments/booking/<int:booking_id>")
api.add_resource(PaymentStatsResource, "/payments/stats")
api.add_resource(MpesaCallbackResource, "/payments/mpesa/callback")

# Host Routes
api.add_resource(HostDashboard, "/host/dashboard")
api.add_resource(HostProfile, "/host/profile")
api.add_resource(HostListings, "/host/listings")
api.add_resource(HostListingDetail, "/host/listings/<int:hostel_id>")
api.add_resource(HostRooms, "/host/rooms/<int:hostel_id>")
api.add_resource(HostRoomDetail, "/host/rooms/<int:hostel_id>/<int:room_id>")
api.add_resource(HostBookings, "/host/bookings")
api.add_resource(HostBookingDetail, "/host/bookings/<int:booking_id>")
api.add_resource(HostEarnings, "/host/earnings")
api.add_resource(HostReviews, "/host/reviews")
api.add_resource(HostNotifications, "/host/notifications")
api.add_resource(HostNotificationDetail, "/host/notifications/<int:notification_id>")
api.add_resource(HostVerificationResource, "/host/verification")
api.add_resource(HostSupport, "/host/support")
api.add_resource(HostSupportTickets, "/host/support/tickets")
api.add_resource(HostAnalytics, "/host/analytics")

# Host Availability Routes
api.add_resource(HostAvailability, "/host/availability")
api.add_resource(HostHostelAvailability, "/host/availability/<int:hostel_id>")
api.add_resource(HostRoomAvailabilityUpdate, "/host/availability/room/<int:room_id>")
api.add_resource(HostAvailabilityCalendar, "/host/availability/<int:hostel_id>/calendar")

# Booking Routes
api.add_resource(BookingResource, "/bookings")
api.add_resource(BookingDetailResource, "/bookings/<int:booking_id>")
api.add_resource(BookingAvailabilityResource, "/bookings/check-availability")
api.add_resource(BookingCancelResource, "/bookings/<int:booking_id>/cancel")



@app.cli.command("seed")
def seed_command():
    """Seed the database with sample data"""
    with app.app_context():
        seed_database()
    print("Database seeded!")

# JWT Error Handlers - Return proper 401 for expired/invalid tokens
@app.errorhandler(JWTExpiredError)
def handle_jwt_expired(error):
    return {"message": "Token has expired. Please log in again."}, 401

@app.errorhandler(InvalidTokenError)
def handle_jwt_invalid(error):
    return {"message": "Invalid token. Please log in again."}, 401

@app.errorhandler(Exception)
def handle_all_errors(error):
    """Catch-all error handler"""
    # Return 500 for unhandled exceptions
    return {"message": "An unexpected error occurred."}, 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)

