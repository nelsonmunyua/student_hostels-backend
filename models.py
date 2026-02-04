from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
#from sqlalchemy.orm import validate
from datetime import datetime
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

    role = db.Column(
        db.String(20),
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


    