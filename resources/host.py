from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Hostel, Room, Booking, Payment, Review, HostEarning, Notification, SupportTicket
from datetime import datetime, date
from sqlalchemy import func

# ==================== HOST DASHBOARD ====================

class HostDashboardResource(Resource):
    @jwt_required()
    def get(self):
        host_id = get_jwt_identity()
        
        # Get all hostels for this host
        hostels = Hostel.query.filter_by(host_id=host_id).all()
        hostel_ids = [h.id for h in hostels]
        
        # Count statistics
        total_hostels = len(hostels)
        active_hostels = len([h for h in hostels if h.is_active])
        
        # Get all rooms for these hostels
        rooms = Room.query.filter(Room.hostel_id.in_(hostel_ids)).all() if hostel_ids else []
        room_ids = [r.id for r in rooms]
        
        # Get bookings
        bookings = Booking.query.filter(Booking.room_id.in_(room_ids)).all() if room_ids else []
        
        # Calculate earnings
        confirmed_bookings = [b for b in bookings if b.status == 'confirmed' or b.status == 'completed']
        total_earnings = sum(b.total_amount for b in confirmed_bookings)
        
        # Get pending bookings
        pending_bookings = [b for b in bookings if b.status == 'pending']
        
        # Get reviews
        reviews = Review.query.filter(Review.hostel_id.in_(hostel_ids)).all() if hostel_ids else []
        avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0
        
        # Get recent bookings (last 5)
        recent_bookings = Booking.query.filter(
            Booking.room_id.in_(room_ids)
        ).order_by(Booking.created_at.desc()).limit(5).all() if room_ids else []
        
        return {
            "stats": {
                "total_hostels": total_hostels,
                "active_hostels": active_hostels,
                "total_rooms": len(rooms),
                "pending_bookings": len(pending_bookings),
                "total_earnings": total_earnings,
                "avg_rating": round(avg_rating, 1),
                "total_reviews": len(reviews)
            },
            "recent_bookings": [booking.to_dict() for booking in recent_bookings]
        }

# ==================== HOST PROFILE ====================

class HostProfileResource(Resource):
    @jwt_required()
    def get(self):
        from models import User
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict()
    
    @jwt_required()
    def put(self):
        from models import User
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
        
        data = request.get_json()
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.phone = data.get('phone', user.phone)
        
        db.session.commit()
        return user.to_dict()

# ==================== HOST LISTINGS ====================

class HostListingsResource(Resource):
    @jwt_required()
    def get(self):
        host_id = get_jwt_identity()
        hostels = Hostel.query.filter_by(host_id=host_id).all()
        
        result = []
        for hostel in hostels:
            rooms = Room.query.filter_by(hostel_id=hostel.id).all()
            hostel_dict = hostel.to_dict()
            hostel_dict['rooms'] = [room.to_dict() for room in rooms]
            hostel_dict['total_rooms'] = len(rooms)
            hostel_dict['available_rooms'] = sum(1 for r in rooms if r.is_available)
            result.append(hostel_dict)
        
        return {"hostels": result}
    
    @jwt_required()
    def post(self):
        host_id = get_jwt_identity()
        data = request.get_json()
        
        # Create hostel
        hostel = Hostel(
            host_id=host_id,
            name=data.get('name'),
            description=data.get('description'),
            location=data.get('location'),
            latitude=data.get('latitude', 0),
            longitude=data.get('longitude', 0),
            amenities=data.get('amenities', []),
            rules=data.get('rules', ''),
            images=data.get('images', []),
            is_verified=False,
            is_active=data.get('is_active', True)
        )
        db.session.add(hostel)
        db.session.commit()
        
        return {
            "message": "Hostel created successfully",
            "hostel": hostel.to_dict()
        }, 201


class HostListingDetailResource(Resource):
    @jwt_required()
    def get(self, hostel_id):
        host_id = get_jwt_identity()
        hostel = Hostel.query.filter_by(id=hostel_id, host_id=host_id).first()
        
        if not hostel:
            return {"error": "Hostel not found"}, 404
        
        rooms = Room.query.filter_by(hostel_id=hostel.id).all()
        reviews = Review.query.filter_by(hostel_id=hostel.id).all()
        
        result = hostel.to_dict()
        result['rooms'] = [room.to_dict() for room in rooms]
        result['reviews'] = [review.to_dict() for review in reviews]
        
        return result
    
    @jwt_required()
    def put(self, hostel_id):
        host_id = get_jwt_identity()
        hostel = Hostel.query.filter_by(id=hostel_id, host_id=host_id).first()
        
        if not hostel:
            return {"error": "Hostel not found"}, 404
        
        data = request.get_json()
        hostel.name = data.get('name', hostel.name)
        hostel.description = data.get('description', hostel.description)
        hostel.location = data.get('location', hostel.location)
        hostel.latitude = data.get('latitude', hostel.latitude)
        hostel.longitude = data.get('longitude', hostel.longitude)
        hostel.amenities = data.get('amenities', hostel.amenities)
        hostel.rules = data.get('rules', hostel.rules)
        hostel.images = data.get('images', hostel.images)
        hostel.is_active = data.get('is_active', hostel.is_active)
        
        db.session.commit()
        
        return {
            "message": "Hostel updated successfully",
            "hostel": hostel.to_dict()
        }
    
    @jwt_required()
    def delete(self, hostel_id):
        host_id = get_jwt_identity()
        hostel = Hostel.query.filter_by(id=hostel_id, host_id=host_id).first()
        
        if not hostel:
            return {"error": "Hostel not found"}, 404
        
        db.session.delete(hostel)
        db.session.commit()
        
        return {"message": "Hostel deleted successfully"}


# ==================== HOST ROOMS ====================

class HostRoomsResource(Resource):
    @jwt_required()
    def get(self, hostel_id):
        host_id = get_jwt_identity()
        hostel = Hostel.query.filter_by(id=hostel_id, host_id=host_id).first()
        
        if not hostel:
            return {"error": "Hostel not found"}, 404
        
        rooms = Room.query.filter_by(hostel_id=hostel_id).all()
        return {"rooms": [room.to_dict() for room in rooms]}
    
    @jwt_required()
    def post(self, hostel_id):
        host_id = get_jwt_identity()
        hostel = Hostel.query.filter_by(id=hostel_id, host_id=host_id).first()
        
        if not hostel:
            return {"error": "Hostel not found"}, 404
        
        data = request.get_json()
        room = Room(
            hostel_id=hostel_id,
            room_type=data.get('room_type'),
            price=data.get('price'),
            capacity=data.get('capacity', 1),
            available_units=data.get('available_units', 1),
            is_available=data.get('is_available', True)
        )
        db.session.add(room)
        db.session.commit()
        
        return {
            "message": "Room created successfully",
            "room": room.to_dict()
        }, 201


class HostRoomDetailResource(Resource):
    @jwt_required()
    def get(self, hostel_id, room_id):
        host_id = get_jwt_identity()
        hostel = Hostel.query.filter_by(id=hostel_id, host_id=host_id).first()
        
        if not hostel:
            return {"error": "Hostel not found"}, 404
        
        room = Room.query.filter_by(id=room_id, hostel_id=hostel_id).first()
        if not room:
            return {"error": "Room not found"}, 404
        
        return room.to_dict()
    
    @jwt_required()
    def put(self, hostel_id, room_id):
        host_id = get_jwt_identity()
        hostel = Hostel.query.filter_by(id=hostel_id, host_id=host_id).first()
        
        if not hostel:
            return {"error": "Hostel not found"}, 404
        
        room = Room.query.filter_by(id=room_id, hostel_id=hostel_id).first()
        if not room:
            return {"error": "Room not found"}, 404
        
        data = request.get_json()
        room.room_type = data.get('room_type', room.room_type)
        room.price = data.get('price', room.price)
        room.capacity = data.get('capacity', room.capacity)
        room.available_units = data.get('available_units', room.available_units)
        room.is_available = data.get('is_available', room.is_available)
        
        db.session.commit()
        
        return {
            "message": "Room updated successfully",
            "room": room.to_dict()
        }
    
    @jwt_required()
    def delete(self, hostel_id, room_id):
        host_id = get_jwt_identity()
        hostel = Hostel.query.filter_by(id=hostel_id, host_id=host_id).first()
        
        if not hostel:
            return {"error": "Hostel not found"}, 404
        
        room = Room.query.filter_by(id=room_id, hostel_id=hostel_id).first()
        if not room:
            return {"error": "Room not found"}, 404
        
        db.session.delete(room)
        db.session.commit()
        
        return {"message": "Room deleted successfully"}


# ==================== HOST BOOKINGS ====================

class HostBookingsResource(Resource):
    @jwt_required()
    def get(self):
        host_id = get_jwt_identity()
        hostels = Hostel.query.filter_by(host_id=host_id).all()
        hostel_ids = [h.id for h in hostels]
        
        if not hostel_ids:
            return {"bookings": [], "message": "No hostels found for this host"}
        
        rooms = Room.query.filter(Room.hostel_id.in_(hostel_ids)).all()
        room_ids = [r.id for r in rooms]
        
        if not room_ids:
            return {"bookings": [], "message": "No rooms found in your hostels"}
        
        bookings = Booking.query.filter(
            Booking.room_id.in_(room_ids)
        ).order_by(Booking.created_at.desc()).all()
        
        if not bookings:
            return {"bookings": [], "message": "No bookings found for your properties"}
        
        # Use the comprehensive to_dict() method from the Booking model
        result = [booking.to_dict() for booking in bookings]
        
        return {
            "bookings": result,
            "total_count": len(result),
            "pending_count": len([b for b in result if b['status'] == 'pending']),
            "confirmed_count": len([b for b in result if b['status'] == 'confirmed']),
            "completed_count": len([b for b in result if b['status'] == 'completed']),
            "cancelled_count": len([b for b in result if b['status'] == 'cancelled'])
        }


class HostBookingDetailResource(Resource):
    @jwt_required()
    def get(self, booking_id):
        host_id = get_jwt_identity()
        hostels = Hostel.query.filter_by(host_id=host_id).all()
        hostel_ids = [h.id for h in hostels]
        
        room = Room.query.filter(Room.hostel_id.in_(hostel_ids)).first()
        if not room:
            return {"error": "Booking not found"}, 404
        
        booking = Booking.query.get(booking_id)
        if not booking or booking.room_id != room.id:
            return {"error": "Booking not found"}, 404
        
        return booking.to_dict()
    
    @jwt_required()
    def patch(self, booking_id):
        host_id = get_jwt_identity()
        hostels = Hostel.query.filter_by(host_id=host_id).all()
        hostel_ids = [h.id for h in hostels]
        
        room = Room.query.filter(Room.hostel_id.in_(hostel_ids)).first()
        if not room:
            return {"error": "Booking not found"}, 404
        
        booking = Booking.query.get(booking_id)
        if not booking or booking.room_id != room.id:
            return {"error": "Booking not found"}, 404
        
        data = request.get_json()
        booking.status = data.get('status', booking.status)
        
        db.session.commit()
        
        return {
            "message": "Booking status updated",
            "booking": booking.to_dict()
        }


# ==================== HOST EARNINGS ====================

class HostEarningsResource(Resource):
    @jwt_required()
    def get(self):
        host_id = get_jwt_identity()
        hostels = Hostel.query.filter_by(host_id=host_id).all()
        hostel_ids = [h.id for h in hostels]
        
        if not hostel_ids:
            return {"earnings": 0, "bookings": []}
        
        rooms = Room.query.filter(Room.hostel_id.in_(hostel_ids)).all()
        room_ids = [r.id for r in rooms]
        
        if not room_ids:
            return {"earnings": 0, "bookings": []}
        
        bookings = Booking.query.filter(
            Booking.room_id.in_(room_ids),
            Booking.status.in_(['confirmed', 'completed'])
        ).all()
        
        total_earnings = sum(b.total_amount for b in bookings)
        
        # Get earnings by month
        earnings_by_month = {}
        for booking in bookings:
            month_key = booking.created_at.strftime('%Y-%m')
            earnings_by_month[month_key] = earnings_by_month.get(month_key, 0) + booking.total_amount
        
        return {
            "total_earnings": total_earnings,
            "total_bookings": len(bookings),
            "earnings_by_month": earnings_by_month,
            "recent_payouts": []
        }


# ==================== HOST REVIEWS ====================

class HostReviewsResource(Resource):
    @jwt_required()
    def get(self):
        host_id = get_jwt_identity()
        hostels = Hostel.query.filter_by(host_id=host_id).all()
        hostel_ids = [h.id for h in hostels]
        
        if not hostel_ids:
            return {"reviews": []}
        
        reviews = Review.query.filter(Review.hostel_id.in_(hostel_ids)).order_by(Review.created_at.desc()).all()
        
        return {"reviews": [review.to_dict() for review in reviews]}


# ==================== HOST ANALYTICS ====================

class HostAnalyticsResource(Resource):
    @jwt_required()
    def get(self):
        host_id = get_jwt_identity()
        hostels = Hostel.query.filter_by(host_id=host_id).all()
        hostel_ids = [h.id for h in hostels]
        
        if not hostel_ids:
            return {
                "total_views": 0,
                "total_bookings": 0,
                "total_revenue": 0,
                "occupancy_rate": 0
            }
        
        rooms = Room.query.filter(Room.hostel_id.in_(hostel_ids)).all()
        room_ids = [r.id for r in rooms]
        
        bookings = Booking.query.filter(Booking.room_id.in_(room_ids)).all()
        confirmed_bookings = [b for b in bookings if b.status in ['confirmed', 'completed']]
        
        # Calculate metrics
        total_revenue = sum(b.total_amount for b in confirmed_bookings)
        total_bookings = len(confirmed_bookings)
        
        # Estimate occupancy (simplified)
        total_units = sum(r.available_units for r in rooms)
        occupied_units = sum(
            r.available_units - sum(1 for b in confirmed_bookings if b.room_id == r.id)
            for r in rooms
        )
        occupancy_rate = (occupied_units / total_units * 100) if total_units > 0 else 0
        
        return {
            "total_views": 0,  # Would need view tracking
            "total_bookings": total_bookings,
            "total_revenue": total_revenue,
            "occupancy_rate": round(occupancy_rate, 1),
            "bookings_by_month": {},
            "revenue_by_month": {}
        }


# ==================== HOST NOTIFICATIONS ====================

class HostNotificationsResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()
        return {"notifications": [n.to_dict() for n in notifications]}
    
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        # Mark all as read
        Notification.query.filter_by(user_id=user_id, is_read=False).update({'is_read': True})
        db.session.commit()
        return {"message": "All notifications marked as read"}


class HostNotificationDetailResource(Resource):
    @jwt_required()
    def put(self, notification_id):
        user_id = get_jwt_identity()
        notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
        
        if not notification:
            return {"error": "Notification not found"}, 404
        
        notification.is_read = True
        db.session.commit()
        
        return notification.to_dict()


# ==================== HOST VERIFICATION ====================

class HostVerificationResource(Resource):
    @jwt_required()
    def get(self):
        from models import HostVerification
        user_id = get_jwt_identity()
        verification = HostVerification.query.filter_by(host_id=user_id).first()
        
        if not verification:
            return {"status": "not_submitted"}
        
        return verification.to_dict()
    
    @jwt_required()
    def post(self):
        from models import HostVerification
        user_id = get_jwt_identity()
        data = request.get_json()
        
        verification = HostVerification(
            host_id=user_id,
            document_type=data.get('document_type'),
            document_url=data.get('document_url'),
            status='pending'
        )
        db.session.add(verification)
        db.session.commit()
        
        return {
            "message": "Verification submitted successfully",
            "verification": verification.to_dict()
        }, 201


# ==================== HOST SUPPORT ====================

class HostSupportResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        tickets = SupportTicket.query.filter_by(user_id=user_id).order_by(SupportTicket.created_at.desc()).all()
        return {"tickets": [t.to_dict() for t in tickets]}
    
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        
        ticket = SupportTicket(
            user_id=user_id,
            subject=data.get('subject'),
            message=data.get('message'),
            status='open'
        )
        db.session.add(ticket)
        db.session.commit()
        
        return {
            "message": "Support ticket created successfully",
            "ticket": ticket.to_dict()
        }, 201


# ==================== HOST AVAILABILITY ====================

class HostAvailabilityResource(Resource):
    @jwt_required()
    def get(self):
        host_id = get_jwt_identity()
        hostels = Hostel.query.filter_by(host_id=host_id).all()
        
        result = []
        for hostel in hostels:
            rooms = Room.query.filter_by(hostel_id=hostel.id).all()
            hostel_dict = hostel.to_dict()
            hostel_dict['rooms'] = [room.to_dict() for room in rooms]
            result.append(hostel_dict)
        
        return {"hostels": result}


class HostAvailabilityDetailResource(Resource):
    @jwt_required()
    def get(self, hostel_id):
        host_id = get_jwt_identity()
        hostel = Hostel.query.filter_by(id=hostel_id, host_id=host_id).first()
        
        if not hostel:
            return {"error": "Hostel not found"}, 404
        
        rooms = Room.query.filter_by(hostel_id=hostel_id).all()
        
        return {
            "hostel": hostel.to_dict(),
            "rooms": [room.to_dict() for room in rooms]
        }


