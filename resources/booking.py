from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from sqlalchemy import and_, or_

from models import db, User, Hostel, Room, Booking, Payment

# =========================
# BOOKING MANAGEMENT
# =========================

class BookingResource(Resource):
    """Create and manage bookings"""
    
    @jwt_required()
    def post(self):
        """Create a new booking"""
        user_id = get_jwt_identity()
        
        data = request.get_json()
        
        # Accept both naming conventions (frontend uses accommodation_id, hostel_id)
        hostel_id = data.get('hostel_id') or data.get('accommodation_id')
        room_id = data.get('room_id')
        # Accept both date formats
        start_date = data.get('start_date') or data.get('check_in')
        end_date = data.get('end_date') or data.get('check_out')
        
        # Validate required fields
        if not hostel_id or not start_date or not end_date:
            return {"message": "hostel_id (or accommodation_id), start_date (or check_in), and end_date (or check_out) are required"}, 400
        
        # Parse dates
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return {"message": "Invalid date format. Use YYYY-MM-DD"}, 400
        
        # Validate dates
        if end_date <= start_date:
            return {"message": "End date must be after start date"}, 400
        
        # Get hostel
        hostel = Hostel.query.get(hostel_id)
        if not hostel:
            return {"message": "Hostel not found"}, 404
        
        # Get room (use first available if not specified)
        if room_id:
            room = Room.query.filter_by(id=room_id, hostel_id=hostel_id).first()
        else:
            room = Room.query.filter_by(
                hostel_id=hostel_id, 
                is_available=True
            ).first()
        
        if not room:
            return {"message": "No available rooms at this hostel"}, 400
        
        # Check if room has available units
        if room.available_units < 1:
            return {"message": "Room is fully booked"}, 400
        
        # Check for conflicting bookings
        conflicting = Booking.query.filter(
            and_(
                Booking.room_id == room.id,
                Booking.status.in_(['pending', 'confirmed']),
                or_(
                    and_(
                        Booking.start_date <= start_date,
                        Booking.end_date > start_date
                    ),
                    and_(
                        Booking.start_date < end_date,
                        Booking.end_date >= end_date
                    ),
                    and_(
                        Booking.start_date >= start_date,
                        Booking.end_date <= end_date
                    )
                )
            )
        ).first()
        
        if conflicting:
            return {"message": "Room is not available for the selected dates"}, 400
        
        # Calculate total amount (price is per month)
        days = (end_date - start_date).days
        months = max(1, days // 30)  # Minimum 1 month
        total_amount = room.price * months
        
        # Create booking
        booking = Booking(
            student_id=user_id,
            room_id=room.id,
            start_date=start_date,
            end_date=end_date,
            status='pending',
            total_amount=total_amount
        )
        
        db.session.add(booking)
        db.session.commit()
        
        return {
            "message": "Booking created successfully",
            "booking": {
                'id': booking.id,
                'hostel_id': hostel.id,
                'hostel_name': hostel.name,
                'room_id': room.id,
                'room_type': room.room_type,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'total_amount': total_amount,
                'status': booking.status,
                'created_at': booking.created_at.isoformat()
            }
        }, 201
    
    @jwt_required()
    def get(self):
        """Get user's bookings"""
        user_id = get_jwt_identity()
        
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        status = request.args.get('status')
        
        query = Booking.query.filter_by(student_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        pagination = query.order_by(Booking.created_at.desc()).paginate(
            page=page,
            per_page=limit,
            error_out=False
        )
        
        bookings = []
        for booking in pagination.items:
            room = booking.room
            hostel = room.hostel if room else None
            
            payment = Payment.query.filter_by(booking_id=booking.id).first()
            
            bookings.append({
                'id': booking.id,
                'hostel_id': hostel.id if hostel else None,
                'hostel_name': hostel.name if hostel else 'Unknown',
                'location': hostel.location if hostel else '',
                'room_type': room.room_type if room else None,
                'start_date': booking.start_date.isoformat() if booking.start_date else None,
                'end_date': booking.end_date.isoformat() if booking.end_date else None,
                'total_amount': booking.total_amount,
                'status': booking.status,
                'payment_status': payment.status if payment else 'pending',
                'created_at': booking.created_at.isoformat() if booking.created_at else None
            })
        
        return {
            'bookings': bookings,
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages
        }, 200


class BookingDetailResource(Resource):
    """Get single booking details"""
    
    @jwt_required()
    def get(self, booking_id):
        user_id = get_jwt_identity()
        
        booking = Booking.query.filter_by(
            id=booking_id,
            student_id=user_id
        ).first_or_404()
        
        room = booking.room
        hostel = room.hostel if room else None
        payment = Payment.query.filter_by(booking_id=booking.id).first()
        
        return {
            'id': booking.id,
            'hostel_id': hostel.id if hostel else None,
            'hostel_name': hostel.name if hostel else 'Unknown',
            'location': hostel.location if hostel else '',
            'room_id': room.id if room else None,
            'room_type': room.room_type if room else None,
            'price_per_month': room.price if room else 0,
            'start_date': booking.start_date.isoformat() if booking.start_date else None,
            'end_date': booking.end_date.isoformat() if booking.end_date else None,
            'total_amount': booking.total_amount,
            'status': booking.status,
            'payment_status': payment.status if payment else 'pending',
            'payment_method': payment.method if payment else None,
            'payment_reference': payment.reference if payment else None,
            'created_at': booking.created_at.isoformat() if booking.created_at else None
        }, 200


class BookingAvailabilityResource(Resource):
    """Check room availability"""
    
    def post(self):
        """Check room availability - no auth required for public availability check"""
        data = request.get_json()
        hostel_id = data.get('hostel_id') if data else None
        room_id = data.get('room_id') if data else None
        start_date = data.get('start_date') if data else None
        end_date = data.get('end_date') if data else None
        
        if not hostel_id or not start_date or not end_date:
            return {"message": "hostel_id, start_date, and end_date are required"}, 400
        
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return {"message": "Invalid date format. Use YYYY-MM-DD"}, 400
        
        # Get available rooms
        rooms_query = Room.query.filter_by(
            hostel_id=hostel_id,
            is_available=True
        )
        
        if room_id:
            rooms_query = rooms_query.filter_by(id=room_id)
        
        rooms = rooms_query.all()
        
        available_rooms = []
        for room in rooms:
            # Check for conflicting bookings
            conflicting = Booking.query.filter(
                and_(
                    Booking.room_id == room.id,
                    Booking.status.in_(['pending', 'confirmed']),
                    or_(
                        and_(
                            Booking.start_date <= start_date,
                            Booking.end_date > start_date
                        ),
                        and_(
                            Booking.start_date < end_date,
                            Booking.end_date >= end_date
                        ),
                        and_(
                            Booking.start_date >= start_date,
                            Booking.end_date <= end_date
                        )
                    )
                )
            ).first()
            
            if not conflicting and room.available_units > 0:
                # Calculate price
                days = (end_date - start_date).days
                months = max(1, days // 30)
                total_price = room.price * months
                
                available_rooms.append({
                    'id': room.id,
                    'room_type': room.room_type,
                    'price': room.price,
                    'capacity': room.capacity,
                    'available_units': room.available_units,
                    'total_price': total_price
                })
        
        return {
            'available': len(available_rooms) > 0,
            'rooms': available_rooms,
            'message': f"{len(available_rooms)} room(s) available" if available_rooms else "No rooms available"
        }, 200


class BookingCancelResource(Resource):
    """Cancel a booking"""
    
    @jwt_required()
    def post(self, booking_id):
        user_id = get_jwt_identity()
        
        booking = Booking.query.filter_by(
            id=booking_id,
            student_id=user_id
        ).first_or_404()
        
        if booking.status == 'cancelled':
            return {"message": "Booking is already cancelled"}, 400
        
        if booking.status == 'completed':
            return {"message": "Cannot cancel a completed booking"}, 400
        
        data = request.get_json() or {}
        reason = data.get('reason', '')
        
        booking.status = 'cancelled'
        booking.cancel_reason = reason
        
        db.session.commit()
        
        return {
            "message": "Booking cancelled successfully",
            "booking": {
                'id': booking.id,
                'status': booking.status,
                'cancel_reason': booking.cancel_reason
            }
        }, 200


class BookingPriceCalculationResource(Resource):
    """Calculate booking price without creating booking"""
    
    @jwt_required()
    def post(self):
        """Calculate the price for a potential booking"""
        data = request.get_json()
        
        # Accept both naming conventions
        hostel_id = data.get('hostel_id') or data.get('accommodation_id')
        room_id = data.get('room_id')
        start_date = data.get('start_date') or data.get('check_in')
        end_date = data.get('end_date') or data.get('check_out')
        
        if not hostel_id or not start_date or not end_date:
            return {"message": "hostel_id, start_date, and end_date are required"}, 400
        
        # Parse dates
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return {"message": "Invalid date format. Use YYYY-MM-DD"}, 400
        
        if end_date <= start_date:
            return {"message": "End date must be after start date"}, 400
        
        # Get hostel
        hostel = Hostel.query.get(hostel_id)
        if not hostel:
            return {"message": "Hostel not found"}, 404
        
        # Get room
        if room_id:
            room = Room.query.filter_by(id=room_id, hostel_id=hostel_id).first()
        else:
            room = Room.query.filter_by(hostel_id=hostel_id, is_available=True).first()
        
        if not room:
            return {"message": "No available rooms at this hostel"}, 400
        
        # Calculate price
        days = (end_date - start_date).days
        nights = days  # Assuming price is per night
        subtotal = room.price * nights
        total_price = subtotal  # Can add tax, fees, etc. here
        
        return {
            'nights': nights,
            'price_per_night': room.price,
            'subtotal': subtotal,
            'total_price': total_price,
            'room_type': room.room_type
        }, 200

