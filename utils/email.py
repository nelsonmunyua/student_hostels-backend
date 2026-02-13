import os
import smtplib
import socket
from threading import Thread
from flask_mail import Message
from flask import current_app, url_for
from itsdangerous import URLSafeTimedSerializer


# ---------------------------------------
# TOKEN GENERATOR (Email Verification / Reset)
# ---------------------------------------

def generate_email_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt="email-confirm-salt")


def confirm_email_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token,
            salt="email-confirm-salt",
            max_age=expiration
        )
    except Exception:
        return None

    return email


# ---------------------------------------
# SEND EMAIL HELPER (With Timeout & Non-blocking)
# ---------------------------------------

def send_email(subject, recipients, html_body):
    """
    Send email with timeout handling and non-blocking execution.
    Returns True if email was sent (or queued), False if skipped.
    """
    # Check if mail is configured before trying to send
    mail_server = current_app.config.get("MAIL_SERVER")
    mail_username = current_app.config.get("MAIL_USERNAME")
    
    if not mail_server or not mail_username:
        print(f"Email not configured. Skipping email: {subject} to {recipients}")
        return False
    
    mail = current_app.extensions.get("mail")

    if not mail:
        print("Flask-Mail not initialized. Skipping email.")
        return False

    # Create message
    msg = Message(
        subject=subject,
        recipients=recipients,
        html=html_body,
        sender=current_app.config.get("MAIL_DEFAULT_SENDER")
    )

    # Send email in a separate thread to prevent blocking the main request
    def _send_async():
        try:
            # Set a short timeout to prevent hanging
            socket.setdefaulttimeout(5)
            with mail.connect() as connection:
                connection.send(msg)
            print(f"Email sent successfully: {subject} to {recipients}")
        except socket.timeout:
            print(f"Email failed (timeout): {subject} to {recipients}")
        except smtplib.SMTPException as e:
            print(f"Email failed (SMTP error): {subject} to {recipients} - {str(e)}")
        except Exception as e:
            print(f"Email failed (error): {subject} to {recipients} - {str(e)}")

    try:
        # Start email sending in background thread
        thread = Thread(target=_send_async)
        thread.daemon = True  # Thread will not prevent app from exiting
        thread.start()
        return True
    except Exception as e:
        print(f"Failed to start email thread: {str(e)}")
        return False


# ---------------------------------------
# EMAIL VERIFICATION
# ---------------------------------------

def send_verification_email(user, token_value):
    #token = generate_email_token(user.email)

    verification_url = url_for(
        "verifyemail",
        token=token_value,
        _external=True
    )

    html = f"""
        <h2>Email Verification</h2>
        <p>Hello {user.first_name},</p>
        <p>Please verify your email by clicking the link below:</p>
        <a href="{verification_url}">Verify Email</a>
        <p>This link expires in 1 hour.</p>
    """

    send_email(
        subject="Verify Your Email",
        recipients=[user.email],
        html_body=html
    )


# ---------------------------------------
# PASSWORD RESET EMAIL
# ---------------------------------------

def send_password_reset_email(user, token_value):
    #token = generate_email_token(user.email)

    reset_url = url_for(
        "resetpassword",
        token=token_value,
        _external=True
    )

    html = f"""
        <h2>Password Reset</h2>
        <p>Hello {user.first_name},</p>
        <p>Click the link below to reset your password:</p>
        <a href="{reset_url}">Reset Password</a>
        <p>This link expires in 1 hour.</p>
    """

    send_email(
        subject="Reset Your Password",
        recipients=[user.email],
        html_body=html
    )
