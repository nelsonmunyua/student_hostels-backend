import os
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
# SEND EMAIL HELPER
# ---------------------------------------

def send_email(subject, recipients, html_body):
    mail = current_app.extensions.get("mail")

    if not mail:
        raise RuntimeError("Flask-Mail not initialized")

    msg = Message(
        subject=subject,
        recipients=recipients,
        html=html_body,
        sender=current_app.config.get("MAIL_DEFAULT_SENDER")
    )

    mail.send(msg)


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
