import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    
    # Frontend URL for redirects
    FRONTEND_URL = os.getenv("FRONTEND_URL", "https://student-hostels-frontend.vercel.app")

    # Flask-Mail Configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", MAIL_USERNAME)

    @staticmethod
    def get_database_url():
        """
        Get database URL with SSL mode for Render PostgreSQL
        """
        database_url = os.getenv("DATABASE_URL")
        
        if not database_url:
            return None
        
        # For Render PostgreSQL, we need to add sslmode=require
        if database_url.startswith("postgresql://") or database_url.startswith("postgres://"):
            # Check if sslmode is already in the URL
            if "?" not in database_url:
                # No query params, add sslmode
                database_url = f"{database_url}?sslmode=require"
            elif "sslmode" not in database_url:
                # Has query params but no sslmode, add it
                database_url = f"{database_url}&sslmode=require"
        
        return database_url
