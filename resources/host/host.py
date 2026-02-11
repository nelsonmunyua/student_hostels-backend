from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import and_, func
from datetime import datetime, timedelta
from models import db, User, Hostel, Room, Booking, Payment, Review, Notification, HostEarning, HostVerification, SupportTicket


def host_required(fn):
    """Decorator to ensure user is a host"""
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'host':
            return {"message": "Host access required"}, 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper


class HostDashboard(Resource):
    """Get host dashboard overview statistics"""
    
    @jwt_required()
    @host_required
    def get(self):
        host_id = get_jwt_identity()
        hostels = Hostel.query.filter_by(host_id=host_id).all()
        hostel_ids = [h.id for h in hostels]
        
        if not hostel_ids:
            return {
                "stats": {
                    "total_hostels": 0,
                    "total_rooms": 0,
                    "active_bookings": 0,
                    "pending_bookings": 0,
                    "total_earnings": 0,
                    "pending_earnings": 0,
                    "avg_rating": 0,
                    "total_reviews": 0
                },
                "recent_bookings": [],
                "recent_reviews": []
            }, 200
        
        # Get all rooms
        rooms = Room.query.filter(Room.hostel_id.in_(hostel_ids)).all()
        room_ids = [r.id for r in rooms]
        
        # Count bookings
        total_bookings = Booking.query.filter(Booking.room_id.in_(room_ids)).count()
        active_bookings = Booking.query.filter(
            and_(
                Booking.room_id.in_(room_ids),
                Booking.status == 'confirmed'
            )
        ).count()
        pending_bookings = Booking.query.filter(
            and_(
                Booking.room_id.in_(room_ids),
                Booking.status == 'pending'
            )
        ).count()
        
        # Calculate earnings
        earnings = db.session.query(
            func.sum(HostEarning.net_amount)
        ).filter(HostEarning.host_id == host_id).scalar() or 0
        
        # Reviews and ratings
        reviews = Review.query.filter(Review.hostel_id.in_(hostel_ids)).all()
        total_reviews = len(reviews)
        avg_rating = sum(r.rating for r in reviews) / total_reviews if reviews else 0
        
        # Recent bookings (last 5)
        recent_bookings_query = Booking.query.join(Room).filter(
            Room.hostel_id.in_(hostel_ids)
        ).order_by(Booking.created_at.desc()).limit(5).all()
        
        recent_bookings = []
        for booking in recent_bookings_query:
            student = User.query.get(booking.student_id)
            room = Room.query.get(booking.room_id)
            hostel = Hostel.query.get(room.hostel_id) if room else None
            
            recent_bookings.append({
                'id': booking.id,
                'student_name': f"{student.first_name} {student.last_name}" if student else "Unknown",
                'hostel_name': hostel.name if hostel else "Unknown",
                'room_type': room.room_type if room else None,
                'check_in': booking.start_date.isoformat() if booking.start_date else None,
                'status': booking.status,
                'total_amount': booking.total_amount,
                'created_at': booking.created_at.isoformat() if booking.created_at else None
            })
        
        # Recent reviews (last 5)
        recent_reviews = Review.query.filter(
            Review.hostel_id.in_(hostel_ids)
        ).order_by(Review.created_at.desc()).limit(5).all()
        
        reviews_list = []
        for review in recent_reviews:
            student = User.query.get(review.user_id)
            hostel = Hostel.query.get(review.hostel_id)
            
            reviews_list.append({
                'id': review.id,
                'hostel_name': hostel.name if hostel else "Unknown",
                'student_name': f"{student.first_name} {student.last_name}" if student else "Unknown",
                'rating': review.rating,
                'comment': review.comment,
                'status': review.status,
                'created_at': review.created_at.isoformat() if review.created_at else None
            })
        
        return {
            "stats": {
                "total_hostels": len(hostels),
                "total_rooms": len(rooms),
                "total_bookings": total_bookings,
                "active_bookings": active_bookings,
                "pending_bookings": pending_bookings,
                "total_earnings": int(earnings),
                "avg_rating": round(avg_rating, 1),
                "total_reviews": total_reviews,
                "verified": User.query.get(host_id).is_verified if User.query.get(host_id) else False
            },
            "recent_bookings": recent_bookings,
            "recent_reviews": reviews_list
        }, 200


class HostProfile(Resource):
    """Get and update host profile"""
    
    @jwt_required()
    @host_required
    def get(self):
        host_id = get_jwt_identity()
        user = User.query.get(host_id)
        
        if not user:
            return {"message": "User not found"}, 404
        
        # Get verification status
        verification = HostVerification.query.filter_by(
            host_id=host_id
        ).order_by(HostVerification.created_at.desc()).first()
        
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
            "is_verified": user.is_verified,
            "verification_status": verification.status if verification else None,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }, 200
    
    @jwt_required()
    @host_required
    def put(self):
        host_id = get_jwt_identity()
        user = User.query.get(host_id)
        
        data = request.get_json()
        
        if data.get('first_name'):
            user.first_name = data['first_name']
        if data.get('last_name'):
            user.last_name = data['last_name']
        if data.get('phone'):
            existing = User.query.filter(
                and_(User.phone == data['phone'], User.id != host_id)
            ).first()
            if existing:
                return {"message": "Phone number already in use"}, 400
            user.phone = data['phone']
        
        db.session.commit()
        
        return {"message": "Profile updated successfully"}, 200


class HostListings(Resource):
    """Get all hostels for the logged-in host"""
    
    @jwt_required()
    @host_required
    def get(self):
        host_id = get_jwt_identity()
        hostels = Hostel.query.filter_by(host_id=host_id).order_by(Hostel.created_at.desc()).all()
        
        result = []
        for h in hostels:
            rooms = Room.query.filter_by(hostel_id=h.id).all()
            reviews = Review.query.filter_by(hostel_id=h.id).all()
            avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0
            
            result.append({
                'id': h.id,
                'name': h.name,
                'location': h.location,
                'description': h.description,
                'is_active': h.is_active,
                'is_verified': h.is_verified,
                'total_rooms': len(rooms),
                'available_rooms': sum(r.available_units for r in rooms),
                'avg_rating': round(avg_rating, 1),
                'total_reviews': len(reviews),
                'created_at': h.created_at.isoformat() if h.created_at else None
            })
        
        return {"hostels": result}, 200
    
    @jwt_required()
    @host_required
    def post(self):
        host_id = get_jwt_identity()
        data = request.get_json()
        
        try:
            hostel = Hostel(
                host_id=host_id,
                name=data.get('name'),
                location=data.get('location'),
                description=data.get('description'),
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                amenities=data.get('amenities'),
                rules=data.get('rules'),
                images=data.get('images') or [],
                is_verified=False,
                is_active=True
            )
            
            db.session.add(hostel)
            db.session.commit()
            
            return {
                "message": "Hostel created",
                "hostel": {'id': hostel.id, 'name': hostel.name}
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed: {str(e)}"}, 400


class HostListingDetail(Resource):
    """Get, update, delete specific hostel"""
    
    @jwt_required()
    @host_required
    def get(self, hostel_id):
        hostel = Hostel.query.filter_by(id=hostel_id, host_id=get_jwt_identity()).first()
        
        if not hostel:
            return {"message": "Hostel not found"}, 404
        
        rooms = Room.query.filter_by(hostel_id=hostel_id).all()
        
        return {
            'id': hostel.id,
            'name': hostel.name,
            'description': hostel.description,
            'location': hostel.location,
            'latitude': hostel.latitude,
            'longitude': hostel.longitude,
            'amenities': hostel.amenities or [],
            'rules': hostel.rules,
            'images': hostel.images or [],
            'is_active': hostel.is_active,
            'is_verified': hostel.is_verified,
            'rooms': [{
                'id': r.id,
                'room_type': r.room_type,
                'price': r.price,
                'capacity': r.capacity,
                'available_units': r.available_units,
                'is_available': r.is_available
            } for r in rooms]
        }, 200
    
    @jwt_required()
    @host_required
    def put(self, hostel_id):
        hostel = Hostel.query.filter_by(id=hostel_id, host_id=get_jwt_identity()).first()
        
        if not hostel:
            return {"message": "Hostel not found"}, 404
        
        data = request.get_json()
        
        if data.get('name'):
            hostel.name = data['name']
        if data.get('location'):
            hostel.location = data['location']
        if 'description' in data:
            hostel.description = data['description']
        if 'amenities' in data:
            hostel.amenities = data['amenities']
        if 'rules' in data:
            hostel.rules = data['rules']
        if 'images' in data:
            hostel.images = data['images']
        
        db.session.commit()
        
        return {"message": "Hostel updated"}, 200
    
    @jwt_required()
    @host_required
    def delete(self, hostel_id):
        hostel = Hostel.query.filter_by(id=hostel_id, host_id=get_jwt_identity()).first()
        
        if not hostel:
            return {"message": "Hostel not found"}, 404
        
        db.session.delete(hostel)
        db.session.commit()
        
        return {"message": "Hostel deleted"}, 200
    
    @jwt_required()
    @host_required
    def patch(self, hostel_id):
        hostel = Hostel.query.filter_by(id=hostel_id, host_id=get_jwt_identity()).first()
        
        if not hostel:
            return {"message": "Hostel not found"}, 404
        
        hostel.is_active = not hostel.is_active
        db.session.commit()
        
        return {
            "message": f"Hostel {'activated' if hostel.is_active else 'deactivated'}",
            "is_active": hostel.is_active
        }, 200


class HostRooms(Resource):
    """Get and add rooms for a hostel"""
    
    @jwt_required()
    @host_required
    def get(self, hostel_id):
        hostel = Hostel.query.filter_by(id=hostel_id, host_id=get_jwt_identity()).first()
        
        if not hostel:
            return {"message": "Hostel not found"}, 404
        
        rooms = Room.query.filter_by(hostel_id=hostel_id).all()
        
        return {
            'rooms': [{
                'id': r.id,
                'room_type': r.room_type,
                'price': r.price,
                'capacity': r.capacity,
                'available_units': r.available_units,
                'is_available': r.is_available
            } for r in rooms]
        }, 200
    
    @jwt_required()
    @host_required
    def post(self, hostel_id):
        hostel = Hostel.query.filter_by(id=hostel_id, host_id=get_jwt_identity()).first()
        
        if not hostel:
            return {"message": "Hostel not found"}, 404
        
        data = request.get_json()
        valid_types = ['single', 'double', 'bed_sitter', 'studio']
        
        if data.get('room_type') not in valid_types:
            return {"message": "Invalid room type"}, 400
        
        try:
            room = Room(
                hostel_id=hostel_id,
                room_type=data['room_type'],
                price=data['price'],
                capacity=data.get('capacity', 1),
                available_units=data.get('available_units', 1),
                is_available=True
            )
            
            db.session.add(room)
            db.session.commit()
            
            return {"message": "Room added", "room": {'id': room.id}}, 201
            
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed: {str(e)}"}, 400


class HostRoomDetail(Resource):
    """Update or delete specific room"""
    
    @jwt_required()
    @host_required
    def put(self, hostel_id, room_id):
        room = Room.query.filter_by(id=room_id, hostel_id=hostel_id).first()
        
        if not room:
            return {"message": "Room not found"}, 404
        
        data = request.get_json()
        
        if data.get('room_type'):
            room.room_type = data['room_type']
        if data.get('price') is not None:
            room.price = data['price']
        if data.get('capacity') is not None:
            room.capacity = data['capacity']
        if data.get('available_units') is not None:
            room.available_units = data['available_units']
            room.is_available = data['available_units'] > 0
        
        db.session.commit()
        
        return {"message": "Room updated"}, 200
    
    @jwt_required()
    @host_required
    def delete(self, hostel_id, room_id):
        room = Room.query.filter_by(id=room_id, hostel_id=hostel_id).first()
        
        if not room:
            return {"message": "Room not found"}, 404
        
        db.session.delete(room)
        db.session.commit()
        
        return {"message": "Room deleted"}, 200


class HostBookings(Resource):
    """Get all bookings for host's properties"""
    
    @jwt_required()
    @host_required
    def get(self):
        host_id = get_jwt_identity()
        hostel_ids = [h.id for h in Hostel.query.filter_by(host_id=host_id).all()]
        
        if not hostel_ids:
            return {'bookings': []}, 200
        
        room_ids = [r.id for r in Room.query.filter(Room.hostel_id.in_(hostel_ids)).all()]
        
        if not room_ids:
            return {'bookings': []}, 200
        
        bookings = Booking.query.filter(
            Booking.room_id.in_(room_ids)
        ).order_by(Booking.created_at.desc()).all()
        
        result = []
        for b in bookings:
            student = User.query.get(b.student_id)
            room = Room.query.get(b.room_id)
            
            result.append({
                'id': b.id,
                'student_name': f"{student.first_name} {student.last_name}" if student else "Unknown",
                'student_email': student.email if student else None,
                'room_type': room.room_type if room else None,
                'check_in': b.start_date.isoformat() if b.start_date else None,
                'check_out': b.end_date.isoformat() if b.end_date else None,
                'status': b.status,
                'total_amount': b.total_amount,
                'created_at': b.created_at.isoformat() if b.created_at else None
            })
        
        return {'bookings': result}, 200


class HostBookingDetail(Resource):
    """Get and update specific booking"""
    
    @jwt_required()
    @host_required
    def get(self, booking_id):
        booking = Booking.query.get(booking_id)
        
        if not booking:
            return {"message": "Booking not found"}, 404
        
        student = User.query.get(booking.student_id)
        
        return {
            'id': booking.id,
            'student_name': f"{student.first_name} {student.last_name}" if student else "Unknown",
            'student_email': student.email if student else None,
            'student_phone': student.phone if student else None,
            'check_in': booking.start_date.isoformat() if booking.start_date else None,
            'status': booking.status,
            'total_amount': booking.total_amount
        }, 200
    
    @jwt_required()
    @host_required
    def patch(self, booking_id):
        booking = Booking.query.get(booking_id)
        
        if not booking:
            return {"message": "Booking not found"}, 404
        
        data = request.get_json()
        
        if data.get('status') in ['pending', 'confirmed', 'cancelled', 'completed']:
            old_status = booking.status
            booking.status = data['status']
            
            # Update room availability
            if data['status'] == 'confirmed' and old_status == 'pending':
                room = Room.query.get(booking.room_id)
                if room and room.available_units > 0:
                    room.available_units -= 1
            
            if data['status'] == 'cancelled' and old_status == 'confirmed':
                room = Room.query.get(booking.room_id)
                if room:
                    room.available_units += 1
            
            db.session.commit()
            
            # Notify student
            notification = Notification(
                user_id=booking.student_id,
                title="Booking Update",
                message=f"Your booking status is now: {data['status']}",
                is_read=False
            )
            db.session.add(notification)
            db.session.commit()
            
            return {"message": "Booking updated", "status": booking.status}, 200
        
        return {"message": "Invalid status"}, 400


class HostEarnings(Resource):
    """Get host earnings and revenue"""
    
    @jwt_required()
    @host_required
    def get(self):
        host_id = get_jwt_identity()
        
        earnings = HostEarning.query.filter_by(host_id=host_id).all()
        total = sum(e.net_amount for e in earnings) if earnings else 0
        
        # Monthly breakdown
        monthly = []
        for i in range(6):
            month_start = datetime.utcnow().replace(day=1) - timedelta(days=30 * i)
            month_earnings = HostEarning.query.filter(
                and_(
                    HostEarning.host_id == host_id,
                    HostEarning.created_at >= month_start
                )
            ).all()
            monthly.append({
                'month': month_start.strftime('%Y-%m'),
                'amount': sum(e.net_amount for e in month_earnings)
            })
        
        return {
            "total_earnings": total,
            "monthly_earnings": monthly,
            "total_transactions": len(earnings)
        }, 200


class HostReviews(Resource):
    """Get reviews for host's properties"""
    
    @jwt_required()
    @host_required
    def get(self):
        host_id = get_jwt_identity()
        hostel_ids = [h.id for h in Hostel.query.filter_by(host_id=host_id).all()]
        
        reviews = Review.query.filter(
            Review.hostel_id.in_(hostel_ids)
        ).order_by(Review.created_at.desc()).all()
        
        result = []
        for r in reviews:
            student = User.query.get(r.user_id)
            hostel = Hostel.query.get(r.hostel_id)
            
            result.append({
                'id': r.id,
                'hostel_name': hostel.name if hostel else "Unknown",
                'student_name': f"{student.first_name} {student.last_name}" if student else "Unknown",
                'rating': r.rating,
                'comment': r.comment,
                'status': r.status,
                'created_at': r.created_at.isoformat() if r.created_at else None
            })
        
        return {"reviews": result}, 200


class HostNotifications(Resource):
    """Get host notifications"""
    
    @jwt_required()
    @host_required
    def get(self):
        host_id = get_jwt_identity()
        
        notifications = Notification.query.filter_by(
            user_id=host_id
        ).order_by(Notification.created_at.desc()).all()
        
        result = [{
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'is_read': n.is_read,
            'created_at': n.created_at.isoformat() if n.created_at else None
        } for n in notifications]
        
        unread = Notification.query.filter_by(
            user_id=host_id, is_read=False
        ).count()
        
        return {"notifications": result, "unread_count": unread}, 200
    
    @jwt_required()
    @host_required
    def post(self):
        host_id = get_jwt_identity()
        
        Notification.query.filter_by(
            user_id=host_id, is_read=False
        ).update({'is_read': True})
        
        db.session.commit()
        
        return {"message": "All marked as read"}, 200


class HostNotificationDetail(Resource):
    """Mark notification as read"""
    
    @jwt_required()
    @host_required
    def put(self, notification_id):
        host_id = get_jwt_identity()
        
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=host_id
        ).first()
        
        if not notification:
            return {"message": "Notification not found"}, 404
        
        notification.is_read = True
        db.session.commit()
        
        return {"message": "Notification marked as read"}, 200


class HostVerificationResource(Resource):
    """Get and submit host verification"""
    
    @jwt_required()
    @host_required
    def get(self):
        host_id = get_jwt_identity()
        
        user = User.query.get(host_id)
        verification = HostVerification.query.filter_by(
            host_id=host_id
        ).order_by(HostVerification.created_at.desc()).first()
        
        return {
            "is_verified": user.is_verified,
            "status": verification.status if verification else None
        }, 200
    
    @jwt_required()
    @host_required
    def post(self):
        host_id = get_jwt_identity()
        data = request.get_json()
        
        existing = HostVerification.query.filter_by(
            host_id=host_id, status='pending'
        ).first()
        
        if existing:
            return {"message": "Already pending"}, 400
        
        verification = HostVerification(
            host_id=host_id,
            document_type=data.get('document_type'),
            document_url=data.get('document_url'),
            status='pending'
        )
        
        db.session.add(verification)
        db.session.commit()
        
        return {"message": "Verification submitted"}, 201


class HostSupport(Resource):
    """Create support ticket"""
    
    @jwt_required()
    @host_required
    def post(self):
        host_id = get_jwt_identity()
        data = request.get_json()
        
        ticket = SupportTicket(
            user_id=host_id,
            subject=data.get('subject'),
            message=data.get('message'),
            status='open'
        )
        
        db.session.add(ticket)
        db.session.commit()
        
        return {"message": "Ticket created", "ticket_id": ticket.id}, 201


class HostSupportTickets(Resource):
    """Get host's support tickets"""
    
    @jwt_required()
    @host_required
    def get(self):
        host_id = get_jwt_identity()
        
        tickets = SupportTicket.query.filter_by(
            user_id=host_id
        ).order_by(SupportTicket.created_at.desc()).all()
        
        return {
            "tickets": [{
                'id': t.id,
                'subject': t.subject,
                'status': t.status,
                'created_at': t.created_at.isoformat() if t.created_at else None
            } for t in tickets]
        }, 200


class HostAnalytics(Resource):
    """Get detailed analytics for host"""
    
    @jwt_required()
    @host_required
    def get(self):
        host_id = get_jwt_identity()
        hostel_ids = [h.id for h in Hostel.query.filter_by(host_id=host_id).all()]
        
        if not hostel_ids:
            return {'bookings_by_status': {}, 'occupancy_rate': 0}, 200
        
        rooms = Room.query.filter(Room.hostel_id.in_(hostel_ids)).all()
        total_capacity = sum(r.capacity for r in rooms)
        occupied = sum(r.capacity - r.available_units for r in rooms)
        occupancy_rate = (occupied / total_capacity * 100) if total_capacity > 0 else 0
        
        bookings_by_status = {
            s: Booking.query.join(Room).filter(
                and_(
                    Room.hostel_id.in_(hostel_ids),
                    Booking.status == s
                )
            ).count()
            for s in ['pending', 'confirmed', 'cancelled', 'completed']
        }
        
        return {
            'bookings_by_status': bookings_by_status,
            'occupancy_rate': round(occupancy_rate, 1),
            'total_hostels': len(hostel_ids),
            'total_rooms': len(rooms)
        }, 200

