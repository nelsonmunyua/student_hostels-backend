from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required
from functools import wraps
from models import db, User, Hostel, Booking, HostVerification, Payment, Review, Setting
from flask import abort
from datetime import datetime
#from flask import User

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or user.role != "admin":
            abort(403, description="Admin access required")

        return fn(*args, **kwargs)
    return wrapper


class AdminDashboardResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        return {
            "users": User.query.count(),
            "hostels": Hostel.query.count(),
            "bookings": Booking.query.count(),
            "revenue": db.session.query(db.func.sum(Payment.amount)).scalar() or 0,
            "pending_verifications": HostVerification.query.filter_by(status="pending").count()
        }
    
class AdminUsersResource(Resource):
    @jwt_required() 
    @admin_required
    def get(self):
        users = User.query.order_by(User.created_at.desc()).all()
        return [u.to_dict() for u in users]

class AdminUserStatusResource(Resource):
    @jwt_required()
    @admin_required
    def patch(self, user_id):
        user = User.query.get_or_404(user_id)
        user.is_verified = not user.is_verified
        db.session.commit()
        return {"message": "User status updated"}   
 # list all hostels
class AdminHostelsResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        hostels = Hostel.query.order_by(Hostel.created_at.desc()).all()
        return [h.to_dict() for h in hostels]

 # Deactivate listing
class AdminHostelStatusResource(Resource):
    @jwt_required()
    @admin_required
    def patch(self, hostel_id):
        hostel = Hostel.query.get_or_404(hostel_id)
        hostel.is_active = not hostel.is_active
        db.session.commit()
        return {"message": "Listing status updated"}
    
# Booking management
class AdminBookingsResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        bookings = Booking.query.order_by(Booking.created_at.desc()).all()
        return [b.to_dict() for b in bookings]


# Payment management
class AdminPaymentResource(Resource):
    @jwt_required
    @admin_required
    def get(self):
        payments = Payment.query.order_by(Payment.created_at.desc()).all()
        return [p.to_dict() for p in payments]
    
# Refund
class AdminPaymentStatusResourse(Resource):
    @jwt_required()
    @admin_required
    def patch(self, payment_id):
        payment = Payment.query.get_or_404(payment_id)
        payment.status = "refunded"
        db.session.commit()
        return {"message" : "Payment refunded"}

# Reviews moderation
class AdminReviewResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        reviews = Review.query.order_by(Review.created_at.desc()).all()
        return [r.to_dict() for r in reviews] 

# Delete inappropriate review
class AdminReviewDeleteResource(Resource):
    @jwt_required()
    @admin_required           
    def delete(self, review_id):
        review = Review.query.get_or_404(review_id)
        db.session.delete(review)
        db.session.commit()
        return {"message": "Review removed"}
    
# Host verification
class AdminHostVerificationResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
       return HostVerification.query.filter_by(status="pending").all()


# Approve / Reject
class AdminHostVerificationAction(Resource):
    @jwt_required
    @admin_required
    def patch(self, verification_id):
        data = request.get_json()
        verification = HostVerification.query.get_or_404(verification_id)

        verification.status = data["status"]
        verification.reviewed_by = get_jwt_identity
        verification.reviewed_at = datetime.utcnow()

        db.session.commit()
        return {"message": "Verification updated"}

# Analytics
class AdminAnalyticsResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        return {
            "bookings_by_status": {
                s: Booking.query.filter_by(status=s).count()
                for s in ["pending", "confirmed", "cancelled", "completed"]
            },
            "payments_by_status": {
                s: Payment.query.filter_by(status=s).count()
                for s in ["paid", "pending", "failed", "refunded"]
            }
        }             
class AdminSettingsResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        return {s.key: s.value for s in Setting.query.all()}

    @jwt_required()
    @admin_required
    def post(self):
        data = request.get_json()
        for key, value in data.items():
            setting = Setting.query.filter_by(key=key).first()
            if not setting:
                setting = Setting(key=key, value=value)
                db.session.add(setting)
            else:
                setting.value = value
        db.session.commit()
        return {"message": "Settings updated"}

