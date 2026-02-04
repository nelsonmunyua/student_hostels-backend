from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Booking, Accommodation
from datetime import datetime

class StudentDashboard(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        
        total_bookings = Booking.query.filter_by(user_id=user_id).count()
        active_bookings = Booking.query.filter_by(user_id=user_id, status='paid').count()
        
        recent_bookings = Booking.query.filter_by(user_id=user_id)\
            .order_by(Booking.created_at.desc()).limit(3).all()
        
        return {
            "stats": {
                "totalBookings": total_bookings,
                "activeBookings": active_bookings,
                "wishlistCount": 0,
                "reviewsGiven": 0
            },
            "recent_bookings": [b.to_dict() for b in recent_bookings]
        }, 200

class StudentBookingList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        status_filter = request.args.get('status', 'all')
        
        query = Booking.query.filter_by(user_id=user_id)
        
        if status_filter != 'all':
            query = query.filter_by(status=status_filter)
            
        bookings = query.all()
        
        return {
            "bookings": [b.to_dict() for b in bookings]
        }, 200
class StudentBookingList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        status_filter = request.args.get('status', 'all')
        query = Booking.query.filter_by(user_id=user_id)
        if status_filter != 'all':
            query = query.filter_by(status=status_filter)
        bookings = query.all()
        return {"bookings": [b.to_dict() for b in bookings]}, 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        new_booking = Booking(
            user_id=user_id,
            accommodation_id=data.get('accommodation_id'),
            check_in=datetime.fromisoformat(data.get('check_in')),
            check_out=datetime.fromisoformat(data.get('check_out')),
            total_price=data.get('total_price'),
            status='pending'
        )
        db.session.add(new_booking)
        db.session.commit()
        return {"message": "Booking created successfully", "booking": new_booking.to_dict()}, 201