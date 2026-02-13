from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Hostel, Room, Booking, Review
from datetime import datetime


# =========================
# PUBLIC REVIEWS
# =========================

class AccommodationReviews(Resource):
    """Get reviews for an accommodation"""
    
    def get(self, accommodation_id):
        """Get all reviews for an accommodation (public)"""
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        sort = request.args.get('sort', 'newest')
        
        # Get reviews for this accommodation
        query = Review.query.filter_by(hostel_id= accommodation_id)
        
        # Sort reviews
        if sort == 'newest':
            query = query.order_by(Review.created_at.desc())
        elif sort == 'oldest':
            query = query.order_by(Review.created_at.asc())
        elif sort == 'highest':
            query = query.order_by(Review.rating.desc())
        elif sort == 'lowest':
            query = query.order_by(Review.rating.asc())
        
        pagination = query.paginate(
            page=page,
            per_page=limit,
            error_out=False
        )
        
        reviews = []
        for review in pagination.items:
            user = User.query.get(review.user_id)
            reviews.append({
                'id': review.id,
                'rating': review.rating,
                'comment': review.comment,
                'user_name': f"{user.first_name} {user.last_name}" if user else "Anonymous",
                'created_at': review.created_at.isoformat() if review.created_at else None
            })
        
        # Calculate average rating
        all_reviews = Review.query.filter_by(hostel_id=accommodation_id).all()
        avg_rating = sum(r.rating for r in all_reviews) / len(all_reviews) if all_reviews else 0
        
        return {
            'reviews': reviews,
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages,
            'average_rating': round(avg_rating, 1),
            'total_reviews': len(all_reviews)
        }, 200


class ReviewDetail(Resource):
    """Get single review"""
    
    def get(self, review_id):
        """Get a single review"""
        review = Review.query.get_or_404(review_id)
        user = User.query.get(review.user_id)
        
        return {
            'id': review.id,
            'booking_id': review.booking_id,
            'hostel_id': review.hostel_id,
            'rating': review.rating,
            'comment': review.comment,
            'status': review.status,
            'user_name': f"{user.first_name} {user.last_name}" if user else "Anonymous",
            'created_at': review.created_at.isoformat() if review.created_at else None
        }, 200


class CreateReview(Resource):
    """Create a new review"""
    
    @jwt_required()
    def post(self):
        """Create a new review"""
        user_id = get_jwt_identity()
        data = request.get_json()
        
        booking_id = data.get('booking_id')
        accommodation_id = data.get('accommodation_id')
        rating = data.get('rating')
        comment = data.get('comment')
        
        if not rating:
            return {"message": "rating is required"}, 400
        
        if rating < 1 or rating > 5:
            return {"message": "Rating must be between 1 and 5"}, 400
        
        # Check if booking exists and belongs to user
        if booking_id:
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
            
            # Get hostel from booking
            if booking.room and booking.room.hostel:
                accommodation_id = booking.room.hostel.id
        
        if not accommodation_id:
            return {"message": "accommodation_id is required"}, 400
        
        # Create review
        review = Review(
            booking_id=booking_id,
            user_id=user_id,
            hostel_id=accommodation_id,
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


class UpdateReview(Resource):
    """Update a review"""
    
    @jwt_required()
    def put(self, review_id):
        """Update a review"""
        user_id = get_jwt_identity()
        
        review = Review.query.filter_by(
            id=review_id,
            user_id=user_id
        ).first_or_404()
        
        if review.status != 'pending':
            return {"message": "Cannot edit approved/rejected review"}, 400
        
        data = request.get_json()
        
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
        """Delete a review"""
        user_id = get_jwt_identity()
        
        review = Review.query.filter_by(
            id=review_id,
            user_id=user_id
        ).first_or_404()
        
        db.session.delete(review)
        db.session.commit()
        
        return {"message": "Review deleted"}, 200


class ReviewStats(Resource):
    """Get review statistics for an accommodation"""
    
    def get(self, accommodation_id):
        """Get review statistics"""
        reviews = Review.query.filter_by(hostel_id=accommodation_id).all()
        
        if not reviews:
            return {
                'average_rating': 0,
                'total_reviews': 0,
                'rating_distribution': {
                    '5': 0, '4': 0, '3': 0, '2': 0, '1': 0
                }
            }, 200
        
        avg_rating = sum(r.rating for r in reviews) / len(reviews)
        
        # Calculate distribution
        distribution = {'5': 0, '4': 0, '3': 0, '2': 0, '1': 0}
        for review in reviews:
            distribution[str(review.rating)] = distribution.get(str(review.rating), 0) + 1
        
        return {
            'average_rating': round(avg_rating, 1),
            'total_reviews': len(reviews),
            'rating_distribution': distribution
        }, 200


class ReviewAverageRating(Resource):
    """Get average rating for an accommodation"""
    
    def get(self, accommodation_id):
        """Get average rating"""
        reviews = Review.query.filter_by(hostel_id=accommodation_id).all()
        
        if not reviews:
            return {'average_rating': 0, 'total_reviews': 0}, 200
        
        avg_rating = sum(r.rating for r in reviews) / len(reviews)
        
        return {
            'average_rating': round(avg_rating, 1),
            'total_reviews': len(reviews)
        }, 200


class CanReview(Resource):
    """Check if user can review an accommodation"""
    
    @jwt_required()
    def get(self, accommodation_id):
        """Check if user can review"""
        user_id = get_jwt_identity()
        
        # Check if user has a completed booking at this accommodation
        bookings = Booking.query.filter(
            Booking.student_id == user_id,
            Booking.status == 'completed'
        ).join(Room).filter(Room.hostel_id == accommodation_id).all()
        
        can_review = len(bookings) > 0
        
        # Check if already reviewed
        already_reviewed = False
        if can_review:
            for booking in bookings:
                existing = Review.query.filter_by(booking_id=booking.id).first()
                if existing:
                    already_reviewed = True
                    break
        
        return {
            'can_review': can_review and not already_reviewed,
            'already_reviewed': already_reviewed,
            'message': 'You can review this accommodation' if can_review and not already_reviewed else 'You cannot review this accommodation'
        }, 200


class LikeReview(Resource):
    """Like a review"""
    
    @jwt_required()
    def post(self, review_id):
        """Like a review"""
        # In a full implementation, you'd track who liked what
        review = Review.query.get_or_404(review_id)
        return {"message": "Review liked"}, 200
    
    @jwt_required()
    def delete(self, review_id):
        """Unlike a review"""
        review = Review.query.get_or_404(review_id)
        return {"message": "Review unliked"}, 200


class RecentReviews(Resource):
    """Get recent reviews"""
    
    def get(self):
        """Get recent reviews"""
        limit = request.args.get('limit', 10, type=int)
        
        reviews = Review.query.order_by(
            Review.created_at.desc()
        ).limit(limit).all()
        
        items = []
        for review in reviews:
            user = User.query.get(review.user_id)
            hostel = Hostel.query.get(review.hostel_id)
            
            items.append({
                'id': review.id,
                'rating': review.rating,
                'comment': review.comment,
                'user_name': f"{user.first_name} {user.last_name}" if user else "Anonymous",
                'hostel_name': hostel.name if hostel else "Unknown",
                'created_at': review.created_at.isoformat() if review.created_at else None
            })
        
        return {'reviews': items}, 200


class TopRatedAccommodations(Resource):
    """Get top rated accommodations"""
    
    def get(self):
        """Get top rated accommodations"""
        limit = request.args.get('limit', 10, type=int)
        
        hostels = Hostel.query.filter_by(is_active=True).all()
        
        rated_hostels = []
        for hostel in hostels:
            reviews = Review.query.filter_by(hostel_id=hostel.id).all()
            if reviews:
                avg_rating = sum(r.rating for r in reviews) / len(reviews)
                rated_hostels.append({
                    'id': hostel.id,
                    'name': hostel.name,
                    'location': hostel.location,
                    'average_rating': round(avg_rating, 1),
                    'total_reviews': len(reviews),
                    'image': hostel.images[0] if hostel.images else None
                })
        
        # Sort by rating
        rated_hostels.sort(key=lambda x: x['average_rating'], reverse=True)
        
        return {'accommodations': rated_hostels[:limit]}, 200

