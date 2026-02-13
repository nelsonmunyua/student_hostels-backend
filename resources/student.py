from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import and_, or_
from datetime import datetime, timedelta

from models import db, User, Hostel, Room, Booking, Payment, Review, Wishlist, Notification, SupportTicket

#trying out to push from the new branch to the main branch
# =========================
# STUDENT ACCOMMODATIONS
# =========================

class StudentAccommodations(Resource):
    """Get all available accommodations for students"""
    
    def get(self):
        """Public endpoint - no authentication required for viewing accommodations"""
        # Get query parameters from request.args
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 12, type=int)
        location = request.args.get('location')
        min_price = request.args.get('min_price', type=int)
        max_price = request.args.get('max_price', type=int)
        room_type = request.args.get('room_type')
        
        # Try to get user_id from JWT if available (for wishlist check)
        user_id = None
        try:
            user_id = get_jwt_identity()
        except:
            pass  # User not authenticated, that's okay for public endpoint
        
        # Build query - get active and verified hostels with available rooms
        # Using subquery to avoid DISTINCT issues with JSON columns
        from sqlalchemy import select
        room_subquery = select(Room.hostel_id).where(Room.is_available == True).distinct()
        
        query = Hostel.query.filter(
            and_(
                Hostel.is_active == True,
                Hostel.is_verified == True,
                Hostel.id.in_(room_subquery)
            )
        )
        
        # Apply filters
        if location:
            search_term = f"%{location}%"
            query = query.filter(
                or_(
                    Hostel.location.ilike(search_term),
                    Hostel.name.ilike(search_term)
                )
            )
        
        # Get accommodations with pagination
        pagination = query.paginate(
            page=page, 
            per_page=limit,
            error_out=False
        )
        
        accommodations = []
        for hostel in pagination.items:
            # Get rooms for this hostel (filter by price after fetching)
            rooms = Room.query.filter_by(hostel_id=hostel.id, is_available=True).all()
            
            # Apply price filters in memory if needed
            filtered_rooms = rooms
            if min_price:
                filtered_rooms = [r for r in filtered_rooms if r.price >= min_price]
            if max_price:
                filtered_rooms = [r for r in filtered_rooms if r.price <= max_price]
            if room_type:
                filtered_rooms = [r for r in filtered_rooms if r.room_type == room_type]
            
            if not filtered_rooms:
                continue
            
            # Get average rating
            reviews = Review.query.filter_by(hostel_id=hostel.id).all()
            avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0
            
            # Check if in wishlist (only if user is authenticated)
            in_wishlist = False
            if user_id:
                in_wishlist = Wishlist.query.filter_by(
                    user_id=user_id, 
                    hostel_id=hostel.id
                ).first() is not None
            
            # Get rooms and price
            hostel_min_price = min(room.price for room in filtered_rooms) if filtered_rooms else 0
            hostel_room_type = filtered_rooms[0].room_type if filtered_rooms else None
            
            # Ensure amenities is always an array
            amenities = hostel.amenities
            if isinstance(amenities, str):
                import json
                try:
                    amenities = json.loads(amenities)
                except:
                    amenities = []
            elif amenities is None:
                amenities = []
            
            accommodations.append({
                'id': hostel.id,
                'name': hostel.name,
                'description': hostel.description,
                'location': hostel.location,
                'latitude': hostel.latitude,
                'longitude': hostel.longitude,
                'amenities': amenities,
                'images': hostel.images or [],
                'price': hostel_min_price,
                'room_type': hostel_room_type,
                'rating': round(avg_rating, 1),
                'review_count': len(reviews),
                'is_in_wishlist': in_wishlist,
                'available_rooms': sum(room.available_units for room in filtered_rooms) if filtered_rooms else 0,
                # Include individual room details
                'rooms': [{
                    'id': room.id,
                    'room_type': room.room_type,
                    'price': room.price,
                    'capacity': room.capacity,
                    'available_units': room.available_units,
                    'is_available': room.is_available
                } for room in filtered_rooms]
            })
        
        return {
            'accommodations': accommodations,
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }, 200
    
    @jwt_required()
    def post(self):
        """Create accommodation - requires authentication (host only)"""
        # This is for hosts to create accommodations
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'host':
            return {"message": "Only hosts can create accommodations"}, 403
        
        # Implementation for creating accommodations would go here
        return {"message": "Use /host/listings to create accommodations"}, 400


class StudentAccommodationDetail(Resource):
    """Get single accommodation details"""
    
    @jwt_required()
    def get(self, hostel_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role not in ['student', 'host']:
            return {"message": "Unauthorized access"}, 403
        
        hostel = Hostel.query.get_or_404(hostel_id)
        
        # Get reviews
        reviews = Review.query.filter_by(hostel_id=hostel_id).order_by(
            Review.created_at.desc()
        ).limit(10).all()
        
        # Get average rating
        all_reviews = Review.query.filter_by(hostel_id=hostel_id).all()
        avg_rating = sum(r.rating for r in all_reviews) / len(all_reviews) if all_reviews else 0
        
        # Get rooms
        rooms = Room.query.filter_by(hostel_id=hostel_id, is_available=True).all()
        
        # Check if in wishlist
        in_wishlist = Wishlist.query.filter_by(
            user_id=user_id, 
            hostel_id=hostel_id
        ).first() is not None
        
        # Get hostel owner info
        host = User.query.get(hostel.host_id)
        
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
            'is_verified': hostel.is_verified,
            'host': {
                'id': host.id if host else None,
                'name': f"{host.first_name} {host.last_name}" if host else "Unknown",
                'phone': host.phone if host else None
            } if host else None,
            'rooms': [{
                'id': room.id,
                'room_type': room.room_type,
                'price': room.price,
                'capacity': room.capacity,
                'available_units': room.available_units
            } for room in rooms],
            'rating': round(avg_rating, 1),
            'review_count': len(all_reviews),
            'recent_reviews': [{
                'id': review.id,
                'rating': review.rating,
                'comment': review.comment,
                'user_name': f"{User.query.get(review.user_id).first_name if User.query.get(review.user_id) else 'Unknown'} {User.query.get(review.user_id).last_name if User.query.get(review.user_id) else ''}",
                'created_at': review.created_at.isoformat()
            } for review in reviews],
            'is_in_wishlist': in_wishlist
        }, 200


# =========================
# STUDENT WISHLIST
# =========================

class StudentWishlist(Resource):
    """Get student's wishlist"""
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 12, type=int)
        
        # Get wishlist items
        wishlist_query = Wishlist.query.filter_by(user_id=user_id).order_by(
            Wishlist.created_at.desc()
        )
        
        pagination = wishlist_query.paginate(
            page=page,
            per_page=limit,
            error_out=False
        )
        
        items = []
        for item in pagination.items:
            hostel = Hostel.query.get(item.hostel_id)
            if hostel:
                # Get average rating
                reviews = Review.query.filter_by(hostel_id=hostel.id).all()
                avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0
                
                items.append({
                    'id': item.id,
                    'hostel_id': hostel.id,
                    'name': hostel.name,
                    'location': hostel.location,
                    'price': hostel.price,
                    'room_type': hostel.room_type,
                    'images': hostel.images or [],
                    'rating': round(avg_rating, 1),
                    'added_at': item.created_at.isoformat()
                })
        
        return {
            'wishlist': items,
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages
        }, 200
    
    @jwt_required()
    def post(self):
        """Add to wishlist"""
        user_id = get_jwt_identity()
        
        data = request.get_json()
        hostel_id = data.get('hostel_id') if data else None
        
        if not hostel_id:
            return {"message": "hostel_id is required"}, 400
        
        # Check if already in wishlist
        existing = Wishlist.query.filter_by(
            user_id=user_id,
            hostel_id=hostel_id
        ).first()
        
        if existing:
            return {"message": "Already in wishlist"}, 400
        
        wishlist = Wishlist(
            user_id=user_id,
            hostel_id=hostel_id
        )
        
        db.session.add(wishlist)
        db.session.commit()
        
        return {"message": "Added to wishlist"}, 201


class StudentWishlistItem(Resource):
    """Remove from wishlist"""
    
    @jwt_required()
    def delete(self, hostel_id):
        user_id = get_jwt_identity()
        
        wishlist = Wishlist.query.filter_by(
            user_id=user_id,
            hostel_id=hostel_id
        ).first()
        
        if not wishlist:
            return {"message": "Not in wishlist"}, 404
        
        db.session.delete(wishlist)
        db.session.commit()
        
        return {"message": "Removed from wishlist"}, 200
    
    @jwt_required()
    def post(self, hostel_id):
        """Toggle wishlist"""
        user_id = get_jwt_identity()
        
        existing = Wishlist.query.filter_by(
            user_id=user_id,
            hostel_id=hostel_id
        ).first()
        
        if existing:
            db.session.delete(existing)
            db.session.commit()
            return {"message": "Removed from wishlist", "in_wishlist": False}, 200
        else:
            wishlist = Wishlist(user_id=user_id, hostel_id=hostel_id)
            db.session.add(wishlist)
            db.session.commit()
            return {"message": "Added to wishlist", "in_wishlist": True}, 201


class StudentWishlistCheck(Resource):
    """Check if accommodation is in wishlist"""
    
    @jwt_required()
    def get(self, hostel_id):
        user_id = get_jwt_identity()
        
        in_wishlist = Wishlist.query.filter_by(
            user_id=user_id,
            hostel_id=hostel_id
        ).first() is not None
        
        return {"in_wishlist": in_wishlist}, 200


# =========================
# STUDENT REVIEWS
# =========================

class StudentReviews(Resource):
    """Get student's reviews"""
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        status = request.args.get('status')
        
        query = Review.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        pagination = query.order_by(Review.created_at.desc()).paginate(
            page=page,
            per_page=limit,
            error_out=False
        )
        
        reviews = []
        for review in pagination.items:
            hostel = Hostel.query.get(review.hostel_id)
            booking = Booking.query.get(review.booking_id)
            
            reviews.append({
                'id': review.id,
                'hostel_id': review.hostel_id,
                'hostel_name': hostel.name if hostel else 'Unknown',
                'hostel_location': hostel.location if hostel else '',
                'rating': review.rating,
                'comment': review.comment,
                'status': review.status,
                'booking_check_in': booking.start_date.isoformat() if booking and booking.start_date else None,
                'created_at': review.created_at.isoformat()
            })
        
        return {
            'reviews': reviews,
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages
        }, 200
    
    @jwt_required()
    def post(self):
        """Create a review"""
        user_id = get_jwt_identity()
        
        data = request.get_json()
        booking_id = data.get('booking_id') if data else None
        rating = data.get('rating') if data else None
        comment = data.get('comment') if data else None
        
        if not booking_id or not rating:
            return {"message": "booking_id and rating are required"}, 400
        
        # Validate rating
        if rating < 1 or rating > 5:
            return {"message": "Rating must be between 1 and 5"}, 400
        
        # Check if booking exists and belongs to user
        booking = Booking.query.filter_by(
            id=booking_id,
            student_id=user_id
        ).first()
        
        if not booking:
            return {"message": "Booking not found"}, 404
        
        # Check if review already exists
        existing = Review.query.filter_by(booking_id=booking_id).first()
        if existing:
            return {"message": "Review already exists for this booking"}, 400
        
        hostel_id = None
        if booking.room and booking.room.hostel:
            hostel_id = booking.room.hostel.id
        
        review = Review(
            booking_id=booking_id,
            user_id=user_id,
            hostel_id=hostel_id,
            rating=rating,
            comment=comment,
            status='pending'
        )
        
        db.session.add(review)
        db.session.commit()
        
        return {
            "message": "Review submitted successfully",
            "review": {
                'id': review.id,
                'rating': review.rating,
                'comment': review.comment,
                'status': review.status
            }
        }, 201


class StudentReviewDetail(Resource):
    """Get/Update/Delete single review"""
    
    @jwt_required()
    def get(self, review_id):
        user_id = get_jwt_identity()
        
        review = Review.query.filter_by(
            id=review_id,
            user_id=user_id
        ).first_or_404()
        
        hostel = Hostel.query.get(review.hostel_id)
        
        return {
            'id': review.id,
            'booking_id': review.booking_id,
            'hostel_id': review.hostel_id,
            'hostel_name': hostel.name if hostel else 'Unknown',
            'rating': review.rating,
            'comment': review.comment,
            'status': review.status,
            'created_at': review.created_at.isoformat()
        }, 200
    
    @jwt_required()
    def put(self, review_id):
        """Update review (only if pending)"""
        user_id = get_jwt_identity()
        
        review = Review.query.filter_by(
            id=review_id,
            user_id=user_id
        ).first_or_404()
        
        if review.status != 'pending':
            return {"message": "Cannot edit approved/rejected review"}, 400
        
        data = request.get_json()
        
        if data:
            if data.get('rating'):
                rating = data.get('rating')
                if rating < 1 or rating > 5:
                    return {"message": "Rating must be between 1 and 5"}, 400
                review.rating = rating
            
            if 'comment' in data:
                review.comment = data.get('comment')
        
        db.session.commit()
        
        return {"message": "Review updated", "review": {
            'id': review.id,
            'rating': review.rating,
            'comment': review.comment,
            'status': review.status
        }}, 200
    
    @jwt_required()
    def delete(self, review_id):
        """Delete review"""
        user_id = get_jwt_identity()
        
        review = Review.query.filter_by(
            id=review_id,
            user_id=user_id
        ).first_or_404()
        
        db.session.delete(review)
        db.session.commit()
        
        return {"message": "Review deleted"}, 200


class StudentPendingReviews(Resource):
    """Get bookings that can be reviewed"""
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        
        # Get completed bookings without reviews
        bookings = Booking.query.filter(
            and_(
                Booking.student_id == user_id,
                Booking.status == 'completed'
            )
        ).outerjoin(Review).filter(Review.id == None).all()
        
        items = []
        for booking in bookings:
            hostel = None
            if booking.room and booking.room.hostel:
                hostel = booking.room.hostel
            
            items.append({
                'booking_id': booking.id,
                'hostel_id': hostel.id if hostel else None,
                'hostel_name': hostel.name if hostel else 'Unknown',
                'hostel_location': hostel.location if hostel else '',
                'check_in': booking.start_date.isoformat(),
                'check_out': booking.end_date.isoformat() if booking.end_date else None
            })
        
        return {
            'pending_reviews': items,
            'total': len(items)
        }, 200


# =========================
# STUDENT PAYMENTS
# =========================

class StudentPayments(Resource):
    """Get student's payment history"""
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        status = request.args.get('status')
        
        # Get user's bookings with payments
        query = Booking.query.filter_by(student_id=user_id)
        
        if status:
            query = query.filter(status=status)
        
        pagination = query.order_by(Booking.created_at.desc()).paginate(
            page=page,
            per_page=limit,
            error_out=False
        )
        
        payments = []
        for booking in pagination.items:
            payment = Payment.query.filter_by(booking_id=booking.id).first()
            
            hostel = None
            if booking.room and booking.room.hostel:
                hostel = booking.room.hostel
            
            payments.append({
                'id': payment.id if payment else None,
                'payment_reference': payment.reference if payment else None,
                'payment_method': payment.method if payment else None,
                'payment_status': payment.status if payment else 'pending',
                'payment_amount': payment.amount if payment else booking.total_amount,
                'paid_at': payment.paid_at.isoformat() if payment and payment.paid_at else None,
                'booking_id': booking.id,
                'hostel_name': hostel.name if hostel else 'Unknown',
                'location': hostel.location if hostel else '',
                'check_in': booking.start_date.isoformat(),
                'check_out': booking.end_date.isoformat() if booking.end_date else None,
                'booking_status': booking.status,
                'created_at': booking.created_at.isoformat()
            })
        
        return {
            'payments': payments,
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages
        }, 200


class StudentPaymentStats(Resource):
    """Get payment statistics for student"""
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        
        # Get all payments
        bookings = Booking.query.filter_by(student_id=user_id).all()
        
        total_paid = 0
        pending_amount = 0
        
        for booking in bookings:
            payment = Payment.query.filter_by(
                booking_id=booking.id,
                status='paid'
            ).first()
            
            if payment:
                total_paid += payment.amount
            else:
                pending_amount += booking.total_amount
        
        return {
            'total_paid': total_paid,
            'pending_amount': pending_amount,
            'total_bookings': len(bookings),
            'completed_payments': Payment.query.join(Booking).filter(
                and_(
                    Booking.student_id == user_id,
                    Payment.status == 'paid'
                )
            ).count()
        }, 200


# =========================
# STUDENT NOTIFICATIONS
# =========================

class StudentNotifications(Resource):
    """Get student's notifications"""
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        
        query = Notification.query.filter_by(user_id=user_id)
        
        if unread_only:
            query = query.filter_by(is_read=False)
        
        pagination = query.order_by(Notification.created_at.desc()).paginate(
            page=page,
            per_page=limit,
            error_out=False
        )
        
        notifications = [{
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'is_read': n.is_read,
            'created_at': n.created_at.isoformat()
        } for n in pagination.items]
        
        unread_count = Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).count()
        
        return {
            'notifications': notifications,
            'total': pagination.total,
            'unread_count': unread_count,
            'page': pagination.page,
            'pages': pagination.pages
        }, 200
    
    @jwt_required()
    def post(self):
        """Mark all as read"""
        user_id = get_jwt_identity()
        
        Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).update({'is_read': True})
        
        db.session.commit()
        
        return {"message": "All notifications marked as read"}, 200


class StudentNotificationDetail(Resource):
    """Get single notification or mark as read"""
    
    @jwt_required()
    def get(self, notification_id):
        user_id = get_jwt_identity()
        
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user_id
        ).first_or_404()
        
        return {
            'id': notification.id,
            'title': notification.title,
            'message': notification.message,
            'is_read': notification.is_read,
            'created_at': notification.created_at.isoformat()
        }, 200
    
    @jwt_required()
    def put(self, notification_id):
        """Mark notification as read"""
        user_id = get_jwt_identity()
        
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user_id
        ).first_or_404()
        
        notification.is_read = True
        db.session.commit()
        
        return {"message": "Notification marked as read"}, 200


# =========================
# STUDENT SUPPORT
# =========================

class StudentSupport(Resource):
    """Create support ticket"""
    
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        
        data = request.get_json()
        subject = data.get('subject') if data else None
        message = data.get('message') if data else None
        booking_id = data.get('booking_id') if data else None
        
        if not subject or not message:
            return {"message": "subject and message are required"}, 400
        
        ticket = SupportTicket(
            user_id=user_id,
            subject=subject,
            message=message,
            booking_id=booking_id,
            status='open'
        )
        
        db.session.add(ticket)
        db.session.commit()
        
        return {
            "message": "Support ticket created",
            "ticket_id": ticket.id
        }, 201


class StudentSupportTickets(Resource):
    """Get student's support tickets"""
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        status = request.args.get('status')
        
        query = SupportTicket.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        pagination = query.order_by(SupportTicket.created_at.desc()).paginate(
            page=page,
            per_page=limit,
            error_out=False
        )
        
        tickets = [{
            'id': t.id,
            'subject': t.subject,
            'message': t.message,
            'status': t.status,
            'booking_id': t.booking_id,
            'created_at': t.created_at.isoformat()
        } for t in pagination.items]
        
        return {
            'tickets': tickets,
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages
        }, 200


# =========================
# STUDENT DASHBOARD STATS
# =========================

class StudentDashboardStats(Resource):
    """Get dashboard statistics"""
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        
        # Count bookings
        total_bookings = Booking.query.filter_by(student_id=user_id).count()
        active_bookings = Booking.query.filter_by(
            student_id=user_id,
            status='confirmed'
        ).count()
        pending_bookings = Booking.query.filter_by(
            student_id=user_id,
            status='pending'
        ).count()
        
        # Count wishlist
        wishlist_count = Wishlist.query.filter_by(user_id=user_id).count()
        
        # Count reviews
        reviews_count = Review.query.filter_by(user_id=user_id).count()
        pending_reviews = Review.query.filter_by(
            user_id=user_id,
            status='pending'
        ).count()
        
        # Count notifications
        unread_notifications = Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).count()
        
        # Get recent bookings
        recent_bookings = Booking.query.filter_by(
            student_id=user_id
        ).order_by(Booking.created_at.desc()).limit(5).all()
        
        recent = []
        for booking in recent_bookings:
            hostel = None
            if booking.room and booking.room.hostel:
                hostel = booking.room.hostel
            
            recent.append({
                'id': booking.id,
                'accommodation_title': hostel.name if hostel else 'Unknown',
                'location': hostel.location if hostel else '',
                'check_in': booking.start_date.isoformat(),
                'check_out': booking.end_date.isoformat() if booking.end_date else None,
                'status': booking.status,
                'total_price': booking.total_amount
            })
        
        return {
            'stats': {
                'total_bookings': total_bookings,
                'active_bookings': active_bookings,
                'pending_bookings': pending_bookings,
                'wishlist_count': wishlist_count,
                'reviews_given': reviews_count,
                'pending_reviews': pending_reviews,
                'unread_notifications': unread_notifications
            },
            'recent_bookings': recent
        }, 200


# =========================
# STUDENT BOOKINGS
# =========================

class StudentBookings(Resource):
    """Get student's bookings"""
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        status = request.args.get('status')
        
        # Build query for student's bookings
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
            hostel = None
            room = None
            payment = None
            
            if booking.room:
                room = booking.room
                if room.hostel:
                    hostel = room.hostel
            
            payment = Payment.query.filter_by(booking_id=booking.id).first()
            
            bookings.append({
                'id': booking.id,
                'accommodation_title': hostel.name if hostel else 'Unknown',
                'location': hostel.location if hostel else '',
                'check_in': booking.start_date.isoformat() if booking.start_date else None,
                'check_out': booking.end_date.isoformat() if booking.end_date else None,
                'total_price': booking.total_amount,
                'status': booking.status,
                'payment_status': payment.status if payment else 'pending',
                'room_type': room.room_type if room else None,
                'hostel_id': hostel.id if hostel else None,
                'created_at': booking.created_at.isoformat() if booking.created_at else None
            })
        
        return {
            'bookings': bookings,
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }, 200


class StudentBookingDetail(Resource):
    """Get single booking details"""
    
    @jwt_required()
    def get(self, booking_id):
        user_id = get_jwt_identity()
        
        booking = Booking.query.filter_by(
            id=booking_id,
            student_id=user_id
        ).first_or_404()
        
        hostel = None
        room = None
        payment = None
        
        if booking.room:
            room = booking.room
            if room.hostel:
                hostel = room.hostel
        
        payment = Payment.query.filter_by(booking_id=booking.id).first()
        
        return {
            'id': booking.id,
            'accommodation_title': hostel.name if hostel else 'Unknown',
            'location': hostel.location if hostel else '',
            'address': hostel.address if hostel else None,
            'check_in': booking.start_date.isoformat() if booking.start_date else None,
            'check_out': booking.end_date.isoformat() if booking.end_date else None,
            'total_price': booking.total_amount,
            'status': booking.status,
            'payment_status': payment.status if payment else 'pending',
            'payment_method': payment.method if payment else None,
            'payment_reference': payment.reference if payment else None,
            'room_type': room.room_type if room else None,
            'room_id': room.id if room else None,
            'hostel_id': hostel.id if hostel else None,
            'host_name': f"{hostel.host.first_name} {hostel.host.last_name}" if hostel and hostel.host else None,
            'host_phone': hostel.host.phone if hostel and hostel.host else None,
            'host_email': hostel.host.email if hostel and hostel.host else None,
            'created_at': booking.created_at.isoformat() if booking.created_at else None
        }, 200

