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
    allow_headers=["Content-Type", "Authorization"]
)

# Load configuration
app.config.from_object(Config)

#app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url


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
    AdminReviewStatusResource
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

from resources.host.host import (
    HostDashboard, HostProfile, HostListings, HostListingDetail,
    HostRooms, HostRoomDetail, HostBookings, HostBookingDetail,
    HostEarnings, HostReviews, HostNotifications, HostNotificationDetail,
    HostVerificationResource, HostSupport, HostSupportTickets, HostAnalytics
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

if __name__ == "__main__":
    app.run(debug=True, port=5001)

