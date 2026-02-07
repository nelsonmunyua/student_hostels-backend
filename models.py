from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
#from sqlalchemy.orm import validate
from datetime import datetime

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

#from extensions import db


naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=naming_convention)

db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    phone = db.Column(db.String(20), unique=True, index=True)

    role = db.Column(db.Enum("student", "host", "admin", name="role_type"),
        nullable=False,
        default="student"
    )  # student | host | admin

    is_verified = db.Column(db.Boolean, default=False)

    # Login tracking
    last_login_at = db.Column(db.DateTime)
    login_count = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.now(

    ))
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now(),
        onupdate=datetime.now()
    )

    # Relationships
    tokens = db.relationship(
        "Token",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat()
        }
    
class Token(db.Model):
    __tablename__ = "tokens"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    token = db.Column(db.String(255), unique=True, nullable=False, index=True)

    token_type = db.Column(
        db.String(50),
        nullable=False
    )
    # email_verification | password_reset | revoked

    expires_at = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Hostel(db.Model, SerializerMixin):
    __tablename__ = "hostels"
    serialize_rules = ("-rooms.hostel", "-reviews.hostel",)

    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    location = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    amenities = db.Column(db.JSON)  # wifi, water, security, parking
    rules = db.Column(db.Text)

    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    rooms = db.relationship("Room", backref="hostel", cascade="all, delete-orphan")
    reviews = db.relationship("Review", backref="hostel", lazy=True)


class Room(db.Model, SerializerMixin):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    hostel_id = db.Column(db.Integer, db.ForeignKey("hostels.id"))

    room_type = db.Column(
        db.Enum("single", "double", "bed_sitter", "studio", name="room_types"),
        nullable=False
    )

    price = db.Column(db.Integer, nullable=False)  # monthly price
    capacity = db.Column(db.Integer, default=1)
    available_units = db.Column(db.Integer, default=1)

    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship("Booking", backref="room", lazy=True)

# =========================
# BOOKINGS
# =========================

class Booking(db.Model, SerializerMixin):
    __tablename__ = "bookings"
    serialize_rules = ("-payments.booking",)

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"))

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)

    status = db.Column(
        db.Enum("pending", "confirmed", "cancelled", "completed", name="booking_status"),
        default="pending"
    )

    total_amount = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    payments = db.relationship("Payment", backref="booking", lazy=True)

# =========================
# PAYMENTS
# =========================

class Payment(db.Model, SerializerMixin):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"))

    reference = db.Column(db.String(100), unique=True, index=True)
    method = db.Column(
        db.Enum("mpesa", "card", "bank", name="payment_methods"),
        nullable=False
    )

    amount = db.Column(db.Integer, nullable=False)

    status = db.Column(
        db.Enum("pending", "paid", "failed", "refunded", name="payment_status"),
        default="pending"
    )

    paid_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# =========================
# REVIEWS & RATINGS
# =========================

class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"
    __table_args__ = (
        db.UniqueConstraint("booking_id", name="uq_review_booking"),
    )

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    hostel_id = db.Column(db.Integer, db.ForeignKey("hostels.id"))

    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# =========================
# WISHLIST
# =========================

class Wishlist(db.Model):
    __tablename__ = "wishlists"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    hostel_id = db.Column(db.Integer, db.ForeignKey("hostels.id"))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# =========================
# NOTIFICATIONS
# =========================

class Notification(db.Model, SerializerMixin):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    title = db.Column(db.String(255))
    message = db.Column(db.Text)

    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class RoomAvailability(db.Model):
    __tablename__ = "room_availability"

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"))

    date = db.Column(db.Date, nullable=False)
    is_available = db.Column(db.Boolean, default=True)

    __table_args__ = (
        db.UniqueConstraint("room_id", "date", name="uq_room_date"),
    )

class HostEarning(db.Model):
    __tablename__ = "host_earnings"

    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"))

    gross_amount = db.Column(db.Integer)
    commission = db.Column(db.Integer)
    net_amount = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class HostVerification(db.Model):
    __tablename__ = "host_verifications"

    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    document_type = db.Column(db.String(50))  # ID, Lease, Business Cert
    document_url = db.Column(db.String(255))

    status = db.Column(
        db.Enum("pending", "approved", "rejected", name="verification_status"),
        default="pending"
    )

    reviewed_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    reviewed_at = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SupportTicket(db.Model, SerializerMixin):
    __tablename__ = "support_tickets"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    subject = db.Column(db.String(255))
    message = db.Column(db.Text)

    status = db.Column(
        db.Enum("open", "in_progress", "resolved", "closed", name="ticket_status"),
        default="open"
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Setting(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True)
    value = db.Column(db.String(255))

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


