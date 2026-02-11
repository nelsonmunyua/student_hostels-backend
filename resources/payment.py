from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Booking, Payment
from datetime import datetime
import os
import requests

class PaymentResource(Resource):
    """Handle payment initialization"""

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()

        booking_id = data.get('booking_id')
        amount = data.get('amount')
        payment_method = data.get('payment_method', 'card')

        if not booking_id or not amount:
            return {"message": "booking_id and amount are required"}, 400

        # Verify booking belongs to user
        booking = Booking.query.filter_by(id=booking_id, student_id=user_id).first()
        if not booking:
            return {"message": "Booking not found"}, 404

        # Create payment record
        payment = Payment(
            booking_id=booking_id,
            amount=amount,
            method=payment_method,
            status='pending'
        )

        db.session.add(payment)
        db.session.commit()

        return {
            "message": "Payment initialized",
            "payment_id": payment.id,
            "amount": amount,
            "method": payment_method
        }, 201


class MpesaPaymentResource(Resource):
    """Handle M-Pesa payments"""

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()

        booking_id = data.get('booking_id')
        phone_number = data.get('phone_number')
        amount = data.get('amount')

        if not all([booking_id, phone_number, amount]):
            return {"message": "booking_id, phone_number, and amount are required"}, 400

        # Verify booking belongs to user
        booking = Booking.query.filter_by(id=booking_id, student_id=user_id).first()
        if not booking:
            return {"message": "Booking not found"}, 404

        # Format phone number
        if phone_number.startswith('0'):
            phone_number = '254' + phone_number[1:]
        elif not phone_number.startswith('254'):
            phone_number = '254' + phone_number

        # Get M-Pesa credentials from environment
        consumer_key = os.getenv('MPESA_CONSUMER_KEY')
        consumer_secret = os.getenv('MPESA_CONSUMER_SECRET')
        shortcode = os.getenv('MPESA_SHORTCODE', '174379')
        passkey = os.getenv('MPESA_PASSKEY')

        if not all([consumer_key, consumer_secret, passkey]):
            return {"message": "M-Pesa configuration missing"}, 500

        try:
            # Get access token
            auth_response = requests.get(
                'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials',
                auth=(consumer_key, consumer_secret)
            )
            auth_data = auth_response.json()
            access_token = auth_data.get('access_token')

            if not access_token:
                return {"message": "Failed to get M-Pesa access token"}, 500

            # Generate timestamp and password
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password = shortcode + passkey + timestamp

            # STK Push request
            stk_data = {
                "BusinessShortCode": shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA": phone_number,
                "PartyB": shortcode,
                "PhoneNumber": phone_number,
                "CallBackURL": os.getenv('MPESA_CALLBACK_URL', 'https://yourdomain.com/mpesa/callback'),
                "AccountReference": f"Booking-{booking_id}",
                "TransactionDesc": f"Payment for booking {booking_id}"
            }

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            stk_response = requests.post(
                'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
                json=stk_data,
                headers=headers
            )

            stk_result = stk_response.json()

            if stk_result.get('ResponseCode') == '0':
                # Create payment record
                payment = Payment(
                    booking_id=booking_id,
                    amount=amount,
                    method='mpesa',
                    status='pending',
                    reference=stk_result.get('CheckoutRequestID')
                )

                db.session.add(payment)
                db.session.commit()

                return {
                    "message": "M-Pesa STK push sent successfully",
                    "checkout_request_id": stk_result.get('CheckoutRequestID'),
                    "response_code": stk_result.get('ResponseCode'),
                    "payment_id": payment.id
                }, 200
            else:
                return {
                    "message": "Failed to initiate M-Pesa payment",
                    "error": stk_result.get('ResponseDescription')
                }, 400

        except Exception as e:
            db.session.rollback()
            return {"message": "Payment processing failed", "error": str(e)}, 500


class MpesaStatusResource(Resource):
    """Check M-Pesa payment status"""

    @jwt_required()
    def get(self, checkout_request_id):
        user_id = get_jwt_identity()

        # Find payment by checkout request ID
        payment = Payment.query.filter_by(reference=checkout_request_id).first()
        if not payment:
            return {"message": "Payment not found"}, 404

        # Verify payment belongs to user
        booking = Booking.query.filter_by(id=payment.booking_id, student_id=user_id).first()
        if not booking:
            return {"message": "Unauthorized"}, 403

        # Get M-Pesa credentials
        consumer_key = os.getenv('MPESA_CONSUMER_KEY')
        consumer_secret = os.getenv('MPESA_CONSUMER_SECRET')
        shortcode = os.getenv('MPESA_SHORTCODE', '174379')
        passkey = os.getenv('MPESA_PASSKEY')

        try:
            # Get access token
            auth_response = requests.get(
                'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials',
                auth=(consumer_key, consumer_secret)
            )
            auth_data = auth_response.json()
            access_token = auth_data.get('access_token')

            if not access_token:
                return {"message": "Failed to get access token"}, 500

            # Query payment status
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password = shortcode + passkey + timestamp

            query_data = {
                "BusinessShortCode": shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "CheckoutRequestID": checkout_request_id
            }

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            query_response = requests.post(
                'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query',
                json=query_data,
                headers=headers
            )

            query_result = query_response.json()

            # Update payment status based on response
            if query_result.get('ResponseCode') == '0':
                result_code = query_result.get('ResultCode')
                if result_code == '0':
                    payment.status = 'paid'
                    payment.paid_at = datetime.utcnow()
                    db.session.commit()
                    return {
                        "status": "paid",
                        "message": "Payment successful",
                        "result_code": result_code
                    }
                elif result_code in ['1', '1032', '1037', '2001']:
                    payment.status = 'failed'
                    db.session.commit()
                    return {
                        "status": "failed",
                        "message": "Payment failed",
                        "result_code": result_code
                    }
                else:
                    return {
                        "status": "pending",
                        "message": "Payment still processing",
                        "result_code": result_code
                    }
            else:
                return {
                    "status": "unknown",
                    "message": "Unable to check payment status",
                    "response_code": query_result.get('ResponseCode')
                }

        except Exception as e:
            return {"message": "Status check failed", "error": str(e)}, 500


class CardPaymentResource(Resource):
    """Handle card payments"""

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()

        booking_id = data.get('booking_id')
        amount = data.get('amount')
        card_details = data.get('card_details')

        if not all([booking_id, amount, card_details]):
            return {"message": "booking_id, amount, and card_details are required"}, 400

        # Verify booking belongs to user
        booking = Booking.query.filter_by(id=booking_id, student_id=user_id).first()
        if not booking:
            return {"message": "Booking not found"}, 404

        # In a real implementation, you would integrate with a payment processor like Stripe
        # For now, we'll simulate a successful payment

        try:
            # Create payment record
            payment = Payment(
                booking_id=booking_id,
                amount=amount,
                method='card',
                status='paid',
                paid_at=datetime.utcnow()
            )

            db.session.add(payment)
            db.session.commit()

            return {
                "message": "Card payment processed successfully",
                "payment_id": payment.id,
                "status": "paid",
                "amount": amount
            }, 200

        except Exception as e:
            db.session.rollback()
            return {"message": "Payment processing failed", "error": str(e)}, 500


class StripePaymentResource(Resource):
    """Handle Stripe payments"""

    @jwt_required()
    def post(self, action):
        if action == 'client-secret':
            return self.get_client_secret()
        elif action == 'confirm':
            return self.confirm_payment()
        else:
            return {"message": "Invalid action"}, 400

    def get_client_secret(self):
        user_id = get_jwt_identity()
        data = request.get_json()

        booking_id = data.get('booking_id')
        amount = data.get('amount')

        if not all([booking_id, amount]):
            return {"message": "booking_id and amount are required"}, 400

        # Verify booking belongs to user
        booking = Booking.query.filter_by(id=booking_id, student_id=user_id).first()
        if not booking:
            return {"message": "Booking not found"}, 404

        # In a real implementation, create Stripe PaymentIntent
        # For demo purposes, return a mock client secret
        import uuid
        client_secret = f"pi_mock_{uuid.uuid4()}"

        return {
            "client_secret": client_secret,
            "amount": amount,
            "currency": "kes"
        }, 200

    def confirm_payment(self):
        user_id = get_jwt_identity()
        data = request.get_json()

        payment_intent_id = data.get('payment_intent_id')
        booking_id = data.get('booking_id')

        if not all([payment_intent_id, booking_id]):
            return {"message": "payment_intent_id and booking_id are required"}, 400

        # Verify booking belongs to user
        booking = Booking.query.filter_by(id=booking_id, student_id=user_id).first()
        if not booking:
            return {"message": "Booking not found"}, 404

        # In a real implementation, verify with Stripe
        # For demo, assume payment is successful

        try:
            # Create payment record
            payment = Payment(
                booking_id=booking_id,
                amount=data.get('amount', booking.total_amount),
                method='stripe',
                status='paid',
                reference=payment_intent_id,
                paid_at=datetime.utcnow()
            )

            db.session.add(payment)
            db.session.commit()

            return {
                "message": "Stripe payment confirmed",
                "payment_id": payment.id,
                "status": "paid"
            }, 200

        except Exception as e:
            db.session.rollback()
            return {"message": "Payment confirmation failed", "error": str(e)}, 500


class PaymentDetailResource(Resource):
    """Get payment details"""

    @jwt_required()
    def get(self, payment_id):
        user_id = get_jwt_identity()

        payment = Payment.query.get_or_404(payment_id)

        # Verify payment belongs to user through booking
        booking = Booking.query.filter_by(id=payment.booking_id, student_id=user_id).first()
        if not booking:
            return {"message": "Unauthorized"}, 403

        return {
            "id": payment.id,
            "booking_id": payment.booking_id,
            "reference": payment.reference,
            "method": str(payment.method),
            "amount": payment.amount,
            "status": str(payment.status),
            "paid_at": payment.paid_at.isoformat() if payment.paid_at else None,
            "created_at": payment.created_at.isoformat() if payment.created_at else None
        }, 200


class PaymentByBookingResource(Resource):
    """Get payment by booking ID"""

    @jwt_required()
    def get(self, booking_id):
        user_id = get_jwt_identity()

        # Verify booking belongs to user
        booking = Booking.query.filter_by(id=booking_id, student_id=user_id).first()
        if not booking:
            return {"message": "Booking not found"}, 404

        payment = Payment.query.filter_by(booking_id=booking_id).first()
        if not payment:
            return {"message": "Payment not found"}, 404

        return {
            "id": payment.id,
            "booking_id": payment.booking_id,
            "reference": payment.reference,
            "method": str(payment.method),
            "amount": payment.amount,
            "status": str(payment.status),
            "paid_at": payment.paid_at.isoformat() if payment.paid_at else None,
            "created_at": payment.created_at.isoformat() if payment.created_at else None
        }, 200


class PaymentStatsResource(Resource):
    """Get payment statistics"""

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        # Get user's payments
        payments = Payment.query.join(Booking).filter(Booking.student_id == user_id).all()

        total_paid = sum(p.amount for p in payments if p.status == 'paid')
        pending_amount = sum(p.amount for p in payments if p.status == 'pending')
        completed_payments = sum(1 for p in payments if p.status == 'paid')

        return {
            "total_paid": total_paid,
            "pending_amount": pending_amount,
            "completed_payments": completed_payments
        }, 200


# M-Pesa callback handler (webhook)
class MpesaCallbackResource(Resource):
    def post(self):
        data = request.get_json()

        # Log callback data
        print("M-Pesa Callback:", data)

        # Process callback
        stk_callback = data.get('Body', {}).get('stkCallback', {})
        checkout_request_id = stk_callback.get('CheckoutRequestID')
        result_code = stk_callback.get('ResultCode')
        callback_metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])

        if checkout_request_id:
            payment = Payment.query.filter_by(reference=checkout_request_id).first()

            if payment:
                if result_code == 0:
                    # Payment successful
                    payment.status = 'paid'
                    payment.paid_at = datetime.utcnow()

                    # Extract transaction details from metadata
                    for item in callback_metadata:
                        if item.get('Name') == 'MpesaReceiptNumber':
                            payment.reference = item.get('Value')
                            break

                else:
                    # Payment failed
                    payment.status = 'failed'

                db.session.commit()

        return {"message": "Callback processed"}, 200
