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
        # Get counts for dashboard stats
        total_users = User.query.count()
        total_hostels = Hostel.query.count()
        total_bookings = Booking.query.count()
        pending_verifications = HostVerification.query.filter_by(status="pending").count()
        
        # Calculate revenue from completed payments
        revenue = db.session.query(db.func.sum(Payment.amount)).filter_by(status="paid").scalar() or 0
        
        # Get recent activity counts
        today = datetime.utcnow().date()
        new_users_today = User.query.filter(db.func.date(User.created_at) == today).count()
        new_bookings_today = Booking.query.filter(db.func.date(Booking.created_at) == today).count()
        
        # Get booking status breakdown
        bookings_pending = Booking.query.filter_by(status="pending").count()
        bookings_confirmed = Booking.query.filter_by(status="confirmed").count()
        bookings_completed = Booking.query.filter_by(status="completed").count()
        
        return {
            "users": total_users,
            "hostels": total_hostels,
            "bookings": total_bookings,
            "revenue": revenue,
            "pending_verifications": pending_verifications,
            "stats": {
                "new_users_today": new_users_today,
                "new_bookings_today": new_bookings_today,
                "bookings_pending": bookings_pending,
                "bookings_confirmed": bookings_confirmed,
                "bookings_completed": bookings_completed
            }
        }
    
class AdminUsersResource(Resource):
    @jwt_required() 
    @admin_required
    def get(self):
        users = User.query.order_by(User.created_at.desc()).all()
        # Return plain dictionaries to avoid serialization issues
        return [
            {
                "id": u.id,
                "first_name": u.first_name,
                "last_name": u.last_name,
                "email": u.email,
                "phone": u.phone,
                "role": str(u.role) if u.role else None,  # Enum to string
                "is_verified": bool(u.is_verified),
                "created_at": u.created_at.isoformat() if u.created_at else None
            }
            for u in users
        ]
    
    @jwt_required()
    @admin_required
    def post(self):
        """Create a new user (admin only)"""
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', required=True, help='First name is required')
        parser.add_argument('last_name', required=True, help='Last name is required')
        parser.add_argument('email', required=True, help='Email is required')
        parser.add_argument('phone', required=True, help='Phone number is required')
        parser.add_argument('password', required=True, help='Password is required')
        parser.add_argument('role', required=True, help='Role is required')
        
        data = parser.parse_args()
        
        # Check email uniqueness
        if User.query.filter_by(email=data['email']).first():
            return {"message": "Email already taken", "status": "fail"}, 400
        
        # Check phone uniqueness
        if User.query.filter_by(phone=data['phone']).first():
            return {"message": "Phone number already taken", "status": "fail"}, 400
        
        # Validate role
        if data['role'] not in ['student', 'host', 'admin']:
            return {"message": "Invalid role", "status": "fail"}, 400
        
        # Note: Password should be hashed in production
        from flask_bcrypt import Bcrypt
        bcrypt = Bcrypt()
        
        try:
            user = User(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                phone=data['phone'],
                role=data['role'],
                is_verified=True  # Admin-created users are verified by default
            )
            user.password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            
            db.session.add(user)
            db.session.commit()
            
            return {
                "message": "User created successfully",
                "user": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "phone": user.phone,
                    "role": str(user.role) if user.role else None,
                    "is_verified": bool(user.is_verified),
                    "created_at": user.created_at.isoformat() if user.created_at else None
                }
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {"message": "Failed to create user", "error": str(e)}, 400

class AdminUserStatusResource(Resource):
    @jwt_required()
    @admin_required
    def patch(self, user_id):
        """Toggle user active status"""
        user = User.query.get_or_404(user_id)
        
        # Toggle is_verified status
        user.is_verified = not user.is_verified
        db.session.commit()
        
        return {
            "message": "User status updated",
            "is_verified": user.is_verified
        }
    
    @jwt_required()
    @admin_required
    def delete(self, user_id):
        """Delete a user"""
        user = User.query.get_or_404(user_id)
        
        try:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted successfully"}
        except Exception as e:
            db.session.rollback()
            return {"message": "Failed to delete user", "error": str(e)}, 400

# List all hostels
class AdminHostelsResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        hostels = Hostel.query.order_by(Hostel.created_at.desc()).all()
        # Return plain dictionaries to avoid serialization issues
        return [
            {
                "id": h.id,
                "host_id": int(h.host_id) if h.host_id else None,
                "name": h.name,
                "description": h.description,
                "location": h.location,
                "latitude": float(h.latitude) if h.latitude else None,
                "longitude": float(h.longitude) if h.longitude else None,
                "amenities": h.amenities,  # JSON field - should be serializable
                "rules": h.rules,
                "images": h.images,  # Images array
                "is_verified": bool(h.is_verified),
                "is_active": bool(h.is_active),
                "created_at": h.created_at.isoformat() if h.created_at else None
            }
            for h in hostels
        ]
    
    @jwt_required()
    @admin_required
    def post(self):
        """Create a new hostel"""
        parser = reqparse.RequestParser()
        parser.add_argument('host_id', required=True, help='Host ID is required')
        parser.add_argument('name', required=True, help='Name is required')
        parser.add_argument('location', required=True, help='Location is required')
        parser.add_argument('description', required=False)
        parser.add_argument('amenities', type=dict, required=False)
        parser.add_argument('rules', required=False)
        
        data = parser.parse_args()
        
        try:
            hostel = Hostel(
                host_id=data['host_id'],
                name=data['name'],
                location=data['location'],
                description=data.get('description'),
                amenities=data.get('amenities'),
                rules=data.get('rules'),
                is_verified=True,  # Admin-created are verified by default
                is_active=True
            )
            
            db.session.add(hostel)
            db.session.commit()
            
            return {
                "message": "Hostel created successfully",
                "hostel": {
                    "id": hostel.id,
                    "host_id": int(hostel.host_id) if hostel.host_id else None,
                    "name": hostel.name,
                    "description": hostel.description,
                    "location": hostel.location,
                    "amenities": hostel.amenities,
                    "rules": hostel.rules,
                    "is_verified": bool(hostel.is_verified),
                    "is_active": bool(hostel.is_active),
                    "created_at": hostel.created_at.isoformat() if hostel.created_at else None
                }
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {"message": "Failed to create hostel", "error": str(e)}, 400

class AdminHostelStatusResource(Resource):
    @jwt_required()
    @admin_required
    def patch(self, hostel_id):
        """Toggle hostel active status"""
        hostel = Hostel.query.get_or_404(hostel_id)
        hostel.is_active = not hostel.is_active
        db.session.commit()
        
        return {
            "message": "Listing status updated",
            "is_active": hostel.is_active
        }
    
    @jwt_required()
    @admin_required
    def delete(self, hostel_id):
        """Delete a hostel"""
        hostel = Hostel.query.get_or_404(hostel_id)
        
        try:
            db.session.delete(hostel)
            db.session.commit()
            return {"message": "Hostel deleted successfully"}
        except Exception as e:
            db.session.rollback()
            return {"message": "Failed to delete hostel", "error": str(e)}, 400

# Booking management
class AdminBookingsResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        bookings = Booking.query.order_by(Booking.created_at.desc()).all()
        # Return plain dictionaries to avoid serialization issues
        return [
            {
                "id": b.id,
                "student_id": int(b.student_id) if b.student_id else None,
                "room_id": int(b.room_id) if b.room_id else None,
                "start_date": b.start_date.isoformat() if b.start_date else None,
                "end_date": b.end_date.isoformat() if b.end_date else None,
                "status": str(b.status) if b.status else None,  # Enum to string
                "total_amount": int(b.total_amount) if b.total_amount else 0,
                "created_at": b.created_at.isoformat() if b.created_at else None
            }
            for b in bookings
        ]
    
    @jwt_required()
    @admin_required
    def patch(self, booking_id):
        """Update booking status"""
        parser = reqparse.RequestParser()
        parser.add_argument('status', required=True, help='Status is required')
        
        data = parser.parse_args()
        
        booking = Booking.query.get_or_404(booking_id)
        
        # Validate status
        valid_statuses = ['pending', 'confirmed', 'cancelled', 'completed']
        if data['status'] not in valid_statuses:
            return {"message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}, 400
        
        booking.status = data['status']
        db.session.commit()
        
        return {
            "message": "Booking status updated",
            "status": booking.status
        }

class AdminBookingDetailResource(Resource):
    @jwt_required()
    @admin_required
    def get(self, booking_id):
        """Get booking details"""
        booking = Booking.query.get_or_404(booking_id)
        # Return plain dictionary to avoid serialization issues
        return {
            "id": booking.id,
            "student_id": int(booking.student_id) if booking.student_id else None,
            "room_id": int(booking.room_id) if booking.room_id else None,
            "start_date": booking.start_date.isoformat() if booking.start_date else None,
            "end_date": booking.end_date.isoformat() if booking.end_date else None,
            "status": str(booking.status) if booking.status else None,
            "total_amount": int(booking.total_amount) if booking.total_amount else 0,
            "created_at": booking.created_at.isoformat() if booking.created_at else None
        }
    
    @jwt_required()
    @admin_required
    def delete(self, booking_id):
        """Delete a booking"""
        booking = Booking.query.get_or_404(booking_id)
        
        try:
            db.session.delete(booking)
            db.session.commit()
            return {"message": "Booking deleted successfully"}
        except Exception as e:
            db.session.rollback()
            return {"message": "Failed to delete booking", "error": str(e)}, 400

# Payment management
class AdminPaymentResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        payments = Payment.query.order_by(Payment.created_at.desc()).all()
        # Return plain dictionaries to avoid serialization issues
        # Note: method and status are Enums, need to convert to strings
        result = []
        for p in payments:
            result.append({
                "id": int(p.id),
                "booking_id": int(p.booking_id) if p.booking_id else None,
                "reference": str(p.reference) if p.reference else None,
                "method": str(p.method) if p.method else None,
                "amount": int(p.amount) if p.amount else 0,
                "status": str(p.status) if p.status else None,
                "paid_at": p.paid_at.isoformat() if p.paid_at else None,
                "created_at": p.created_at.isoformat() if p.created_at else None
            })
        return result
    
class AdminPaymentStatusResourse(Resource):
    @jwt_required()
    @admin_required
    def patch(self, payment_id):
        """Update payment status (for refunds)"""
        parser = reqparse.RequestParser()
        parser.add_argument('status', required=True, help='Status is required')
        
        data = parser.parse_args()
        
        payment = Payment.query.get_or_404(payment_id)
        
        # Validate status
        valid_statuses = ['pending', 'paid', 'failed', 'refunded']
        if data['status'] not in valid_statuses:
            return {"message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}, 400
        
        payment.status = data['status']
        
        if data['status'] == 'paid':
            payment.paid_at = datetime.utcnow()
        
        db.session.commit()
        
        return {
            "message": "Payment status updated",
            "status": payment.status
        }

# Reviews moderation
class AdminReviewResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        reviews = Review.query.order_by(Review.created_at.desc()).all()
        # Return plain dictionaries to avoid serialization issues
        return [
            {
                "id": r.id,
                "booking_id": int(r.booking_id) if r.booking_id else None,
                "user_id": int(r.user_id) if r.user_id else None,
                "hostel_id": int(r.hostel_id) if r.hostel_id else None,
                "rating": int(r.rating) if r.rating else 0,
                "comment": r.comment,
                "status": getattr(r, 'status', 'pending'),
                "created_at": r.created_at.isoformat() if r.created_at else None
            }
            for r in reviews
        ]

# Approve/Reject review
class AdminReviewStatusResource(Resource):
    @jwt_required()
    @admin_required
    def patch(self, review_id):
        """Update review status (approve/reject)"""
        parser = reqparse.RequestParser()
        parser.add_argument('action', required=True, help='Action is required')
        
        data = parser.parse_args()
        
        review = Review.query.get_or_404(review_id)
        
        # Map action to status
        action_status_map = {
            'approve': 'approved',
            'reject': 'rejected'
        }
        
        if data['action'] not in action_status_map:
            return {"message": "Invalid action. Must be 'approve' or 'reject'"}, 400
        
        # Store old status for response
        old_status = review.status
        
        review.status = action_status_map[data['action']]
        db.session.commit()
        
        return {
            "message": "Review status updated",
            "old_status": old_status,
            "new_status": review.status
        }

# Delete inappropriate review
class AdminReviewDeleteResource(Resource):
    @jwt_required()
    @admin_required           
    def delete(self, review_id):
        review = Review.query.get_or_404(review_id)
        
        try:
            db.session.delete(review)
            db.session.commit()
            return {"message": "Review removed"}
        except Exception as e:
            db.session.rollback()
            return {"message": "Failed to remove review", "error": str(e)}, 400
    
# Host verification
class AdminHostVerificationResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        """Get all pending verifications"""
        verifications = HostVerification.query.filter_by(status="pending").order_by(HostVerification.created_at.desc()).all()
        # Return plain dictionaries to avoid serialization issues
        return [
            {
                "id": v.id,
                "host_id": int(v.host_id) if v.host_id else None,
                "document_type": v.document_type,
                "document_url": v.document_url,
                "status": str(v.status) if v.status else None,
                "reviewed_by": int(v.reviewed_by) if v.reviewed_by else None,
                "reviewed_at": v.reviewed_at.isoformat() if v.reviewed_at else None,
                "created_at": v.created_at.isoformat() if v.created_at else None
            }
            for v in verifications
        ]
    
    @jwt_required()
    @admin_required
    def get_all(self):
        """Get all verifications (including processed)"""
        verifications = HostVerification.query.order_by(HostVerification.created_at.desc()).all()
        # Return plain dictionaries to avoid serialization issues
        return [
            {
                "id": v.id,
                "host_id": int(v.host_id) if v.host_id else None,
                "document_type": v.document_type,
                "document_url": v.document_url,
                "status": str(v.status) if v.status else None,
                "reviewed_by": int(v.reviewed_by) if v.reviewed_by else None,
                "reviewed_at": v.reviewed_at.isoformat() if v.reviewed_at else None,
                "created_at": v.created_at.isoformat() if v.created_at else None
            }
            for v in verifications
        ]


# Approve / Reject
class AdminHostVerificationAction(Resource):
    @jwt_required()
    @admin_required
    def patch(self, verification_id):
        """Approve or reject a host verification"""
        data = request.get_json()
        
        if not data or 'status' not in data:
            return {"message": "Status is required"}, 400
        
        if data['status'] not in ['approved', 'rejected']:
            return {"message": "Status must be 'approved' or 'rejected'"}, 400
        
        verification = HostVerification.query.get_or_404(verification_id)

        verification.status = data["status"]
        verification.reviewed_by = get_jwt_identity()  # Fixed: Added parentheses
        verification.reviewed_at = datetime.utcnow()

        # Also update the host's verified status if approved
        if data['status'] == 'approved':
            host = User.query.get(verification.host_id)
            if host:
                host.is_verified = True
        
        db.session.commit()
        return {"message": "Verification updated", "status": verification.status}

# Analytics
class AdminAnalyticsResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        """Get comprehensive analytics data"""
        # Booking statistics
        bookings_by_status = {
            s: Booking.query.filter_by(status=s).count()
            for s in ["pending", "confirmed", "cancelled", "completed"]
        }
        
        # Payment statistics
        payments_by_status = {
            s: Payment.query.filter_by(status=s).count()
            for s in ["paid", "pending", "failed", "refunded"]
        }
        
        # Revenue calculation
        total_revenue = db.session.query(db.func.sum(Payment.amount)).filter_by(status="paid").scalar() or 0
        
        # User statistics by role
        users_by_role = {
            'student': User.query.filter_by(role='student').count(),
            'host': User.query.filter_by(role='host').count(),
            'admin': User.query.filter_by(role='admin').count()
        }
        
        # Hostel statistics
        active_hostels = Hostel.query.filter_by(is_active=True).count()
        verified_hostels = Hostel.query.filter_by(is_verified=True).count()
        
        # Monthly trend (simplified - last 6 months)
        import dateutil.relativedelta as relativedelta
        from dateutil import parser
        six_months_ago = datetime.utcnow() - relativedelta.relativedelta(months=6)
        
        monthly_signups_query = db.session.query(
            db.func.date_trunc('month', User.created_at).label('month'),
            db.func.count(User.id).label('count')
        ).filter(User.created_at >= six_months_ago).group_by('month').all()
        
        # Convert to plain Python types
        monthly_signups = []
        for m in monthly_signups_query:
            month_val = m.month
            monthly_signups.append({
                "month": str(month_val) if month_val else None,
                "count": int(m.count) if m.count else 0
            })
        
        return {
            "bookings_by_status": bookings_by_status,
            "payments_by_status": payments_by_status,
            "total_revenue": int(total_revenue) if total_revenue else 0,
            "users_by_role": users_by_role,
            "hostels_stats": {
                "total": Hostel.query.count(),
                "active": active_hostels,
                "verified": verified_hostels
            },
            "monthly_signups": monthly_signups
        }

class AdminSettingsResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        # Convert all settings to plain strings to avoid serialization issues
        settings = {}
        for s in Setting.query.all():
            settings[s.key] = str(s.value) if s.value else ""
        return settings

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
    
    @jwt_required()
    @admin_required
    def delete(self, key):
        """Delete a setting"""
        setting = Setting.query.filter_by(key=key).first()
        if setting:
            db.session.delete(setting)
            db.session.commit()
            return {"message": "Setting deleted"}
        return {"message": "Setting not found"}, 404

