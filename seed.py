# seed.py
import random
from datetime import datetime, timedelta

# Import your models and extensions
from models import db, User, Token, Hostel, Room, Booking, Payment, Review, Wishlist, Notification, RoomAvailability, HostEarning, HostVerification, SupportTicket, Setting
from flask_bcrypt import Bcrypt

# Initialize bcrypt
bcrypt = Bcrypt()

def seed_database():
    """Main seeding function"""
    
    # Clear existing data (optional - comment out in production!)
    print("⚠️  Clearing existing data...")
    clear_database()
    
    print("🌱 Seeding database...")
    
    # Create users
    users = create_users()
    
    # Create settings
    create_settings()
    
    # Create host verifications
    create_host_verifications(users)
    
    # Create hostels with rooms
    hostels_with_rooms = create_hostels_with_rooms(users)
    
    # Create bookings and related data
    bookings = create_bookings(users, hostels_with_rooms)
    
    # Create payments
    create_payments(bookings)
    
    # Create reviews
    create_reviews(users, bookings, hostels_with_rooms)
    
    # Create wishlists
    create_wishlists(users, hostels_with_rooms)
    
    # Create notifications
    create_notifications(users)
    
    # Create room availability
    create_room_availability(hostels_with_rooms)
    
    # Create host earnings
    create_host_earnings(bookings)
    
    # Create support tickets
    create_support_tickets(users)
    
    print("✅ Database seeded successfully!")
    print_summary()

def clear_database():
    """Clear all tables (in reverse order to handle foreign keys)"""
    tables = [
        HostEarning, RoomAvailability, SupportTicket, 
        Wishlist, Notification, Review, Payment, Booking,
        Room, Hostel, HostVerification, Token, Setting, User
    ]
    
    for table in tables:
        try:
            db.session.query(table).delete()
        except:
            pass
    
    db.session.commit()

def create_users():
    """Create sample users"""
    print("👥 Creating users...")
    
    users_data = [
        # Admin users
        {
            "first_name": "Admin",
            "last_name": "System",
            "email": "admin@hostelhub.com",
            "password": "admin123",
            "phone": "+254700000001",
            "role": "admin",
            "is_verified": True,
            "login_count": 50,
            "last_login_at": datetime.now() - timedelta(days=1)
        },
        # Host users
        {
            "first_name": "John",
            "last_name": "Kamau",
            "email": "john.kamau@example.com",
            "password": "host123",
            "phone": "+254711222333",
            "role": "host",
            "is_verified": True,
            "login_count": 25,
            "last_login_at": datetime.now() - timedelta(days=3)
        },
        {
            "first_name": "Sarah",
            "last_name": "Mwangi",
            "email": "sarah.m@example.com",
            "password": "host123",
            "phone": "+254722333444",
            "role": "host",
            "is_verified": True,
            "login_count": 15,
            "last_login_at": datetime.now() - timedelta(days=5)
        },
        {
            "first_name": "David",
            "last_name": "Ochieng",
            "email": "david.o@example.com",
            "password": "host123",
            "phone": "+254733444555",
            "role": "host",
            "is_verified": False,  # Not verified yet
            "login_count": 8,
            "last_login_at": datetime.now() - timedelta(days=10)
        },
        # Student users
        {
            "first_name": "Alice",
            "last_name": "Wanjiru",
            "email": "alice.w@student.com",
            "password": "student123",
            "phone": "+254744555666",
            "role": "student",
            "is_verified": True,
            "login_count": 30,
            "last_login_at": datetime.now() - timedelta(hours=2)
        },
        {
            "first_name": "Brian",
            "last_name": "Omondi",
            "email": "brian.o@student.com",
            "password": "student123",
            "phone": "+254755666777",
            "role": "student",
            "is_verified": True,
            "login_count": 20,
            "last_login_at": datetime.now() - timedelta(days=1)
        },
        {
            "first_name": "Grace",
            "last_name": "Akinyi",
            "email": "grace.a@student.com",
            "password": "student123",
            "phone": "+254766777888",
            "role": "student",
            "is_verified": True,
            "login_count": 12,
            "last_login_at": datetime.now() - timedelta(days=4)
        },
        {
            "first_name": "Peter",
            "last_name": "Mutiso",
            "email": "peter.m@student.com",
            "password": "student123",
            "phone": "+254777888999",
            "role": "student",
            "is_verified": False,  # New student not verified
            "login_count": 3,
            "last_login_at": datetime.now() - timedelta(days=7)
        }
    ]
    
    users = []
    for user_data in users_data:
        user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password_hash=bcrypt.generate_password_hash(user_data["password"]).decode("utf-8"),
            phone=user_data["phone"],
            role=user_data["role"],
            is_verified=user_data["is_verified"],
            login_count=user_data["login_count"],
            last_login_at=user_data["last_login_at"],
            created_at=datetime.now() - timedelta(days=random.randint(30, 180))
        )
        users.append(user)
        db.session.add(user)
    
    db.session.commit()
    return users

def create_settings():
    """Create system settings"""
    print("⚙️  Creating settings...")
    
    settings_data = [
        {"key": "commission_rate", "value": "10"},
        {"key": "min_booking_days", "value": "30"},
        {"key": "max_booking_days", "value": "365"},
        {"key": "auto_cancel_hours", "value": "24"},
        {"key": "app_name", "value": "HostelHub"},
        {"key": "contact_email", "value": "support@hostelhub.com"},
        {"key": "contact_phone", "value": "+254700123456"},
        {"key": "currency", "value": "KES"},
        {"key": "tax_rate", "value": "16"},
        {"key": "max_hostels_per_host", "value": "5"},
        {"key": "review_window_days", "value": "14"},
        {"key": "refund_window_days", "value": "7"},
        {"key": "maintenance_mode", "value": "false"}
    ]
    
    for setting_data in settings_data:
        setting = Setting(
            key=setting_data["key"],
            value=setting_data["value"],
            updated_at=datetime.now()
        )
        db.session.add(setting)
    
    db.session.commit()

def create_host_verifications(users):
    """Create host verification records"""
    print("📋 Creating host verifications...")
    
    hosts = [u for u in users if u.role == "host"]
    
    for host in hosts:
        status_options = ["pending", "approved", "rejected"]
        # Make first host approved, second approved, third pending
        if host.email == "john.kamau@example.com":
            status = "approved"
        elif host.email == "sarah.m@example.com":
            status = "approved"
        else:
            status = "pending"
        
        verification = HostVerification(
            host_id=host.id,
            document_type=random.choice(["ID", "Lease Agreement", "Business Certificate"]),
            document_url=f"https://storage.hostelhub.com/documents/{host.id}/document.pdf",
            status=status,
            reviewed_by=users[0].id if status in ["approved", "rejected"] else None,
            reviewed_at=datetime.now() - timedelta(days=random.randint(1, 30)) if status in ["approved", "rejected"] else None,
            created_at=datetime.now() - timedelta(days=random.randint(10, 60))
        )
        db.session.add(verification)
    
    db.session.commit()

def create_hostels_with_rooms(users):
    """Create hostels with rooms"""
    print("🏨 Creating hostels and rooms...")
    
    hosts = [u for u in users if u.role == "host"]
    hostels_with_rooms = []
    
    # Sample hostels data
    hostels_data = [
        {
            "name": "Campus View Apartments",
            "description": "Modern student apartments with great campus views. Perfect for serious students.",
            "location": "Westlands, Nairobi",
            "latitude": -1.2625,
            "longitude": 36.8022,
            "amenities": ["wifi", "water", "security", "parking", "laundry", "gym", "study_room"],
            "rules": "No pets. No smoking. Quiet hours 10PM-7AM.",
            "is_verified": True,
            "is_active": True,
            "host": hosts[0]
        },
        {
            "name": "Green Valley Hostel",
            "description": "Eco-friendly hostel with beautiful gardens and study spaces.",
            "location": "Kilimani, Nairobi",
            "latitude": -1.2921,
            "longitude": 36.7921,
            "amenities": ["wifi", "water", "security", "parking", "garden", "library"],
            "rules": "Sustainable living encouraged. Recycling mandatory.",
            "is_verified": True,
            "is_active": True,
            "host": hosts[0]
        },
        {
            "name": "University Heights",
            "description": "Affordable accommodation near the university. Great for budget-conscious students.",
            "location": "Kileleshwa, Nairobi",
            "latitude": -1.2710,
            "longitude": 36.7825,
            "amenities": ["wifi", "water", "security", "common_room"],
            "rules": "Visitors allowed until 9PM. Monthly cleaning required.",
            "is_verified": True,
            "is_active": True,
            "host": hosts[1]
        },
        {
            "name": "Digital Nomad Hub",
            "description": "High-speed internet and coworking spaces for tech students.",
            "location": "Upper Hill, Nairobi",
            "latitude": -1.2833,
            "longitude": 36.8167,
            "amenities": ["wifi", "water", "security", "parking", "coworking", "printing"],
            "rules": "24/7 access. Respect quiet zones.",
            "is_verified": False,  # New hostel not verified
            "is_active": True,
            "host": hosts[2]
        }
    ]
    
    # Room types and prices
    room_types = ["single", "double", "bed_sitter", "studio"]
    base_prices = {
        "single": 8000,
        "double": 12000,
        "bed_sitter": 15000,
        "studio": 20000
    }
    
    for hostel_data in hostels_data:
        hostel = Hostel(
            host_id=hostel_data["host"].id,
            name=hostel_data["name"],
            description=hostel_data["description"],
            location=hostel_data["location"],
            latitude=hostel_data["latitude"],
            longitude=hostel_data["longitude"],
            amenities=hostel_data["amenities"],
            rules=hostel_data["rules"],
            is_verified=hostel_data["is_verified"],
            is_active=hostel_data["is_active"],
            created_at=datetime.now() - timedelta(days=random.randint(60, 365))
        )
        db.session.add(hostel)
        db.session.flush()  # Get the hostel ID
        
        # Create rooms for this hostel
        rooms = []
        for i in range(random.randint(5, 15)):  # 5-15 rooms per hostel
            room_type = random.choice(room_types)
            price_variation = random.randint(-1000, 2000)
            
            room = Room(
                hostel_id=hostel.id,
                room_type=room_type,
                price=base_prices[room_type] + price_variation,
                capacity=2 if room_type == "double" else 1,
                available_units=random.randint(0, 3),  # Some rooms might be fully booked
                is_available=random.choice([True, False, True, True]),  # 75% chance available
                created_at=datetime.now() - timedelta(days=random.randint(30, 180))
            )
            rooms.append(room)
            db.session.add(room)
        
        hostels_with_rooms.append({
            "hostel": hostel,
            "rooms": rooms
        })
    
    db.session.commit()
    return hostels_with_rooms

def create_bookings(users, hostels_with_rooms):
    """Create bookings"""
    print("📅 Creating bookings...")
    
    students = [u for u in users if u.role == "student"]
    bookings = []
    
    # Get all rooms
    all_rooms = []
    for hostel_data in hostels_with_rooms:
        all_rooms.extend(hostel_data["rooms"])
    
    # Create bookings for each student
    for student in students:
        num_bookings = random.randint(1, 4)  # 1-4 bookings per student
        
        for _ in range(num_bookings):
            room = random.choice(all_rooms)
            
            # Generate random dates
            start_date = datetime.now() - timedelta(days=random.randint(10, 90))
            end_date = start_date + timedelta(days=random.randint(30, 180))
            
            # Calculate total amount
            months = (end_date - start_date).days / 30
            total_amount = int(room.price * months)
            
            # Booking status
            if end_date < datetime.now():
                status = "completed"
            elif start_date > datetime.now() + timedelta(days=7):
                status = "confirmed"
            else:
                status = random.choice(["pending", "confirmed", "cancelled", "completed"])
            
            booking = Booking(
                student_id=student.id,
                room_id=room.id,
                start_date=start_date.date(),
                end_date=end_date.date(),
                status=status,
                total_amount=total_amount,
                created_at=start_date - timedelta(days=random.randint(1, 10))
            )
            bookings.append(booking)
            db.session.add(booking)
    
    db.session.commit()
    return bookings

def create_payments(bookings):
    """Create payments for bookings"""
    print("💰 Creating payments...")
    
    payment_methods = ["mpesa", "card", "bank"]
    payment_statuses = ["pending", "paid", "failed", "refunded"]
    
    for booking in bookings:
        # Skip cancelled bookings
        if booking.status == "cancelled":
            continue
        
        # Decide number of payments (1 for full, 2-3 for installments)
        num_payments = random.choice([1, 1, 1, 2, 3])  # Mostly single payments
        
        if num_payments == 1:
            amounts = [booking.total_amount]
        else:
            # Split into installments
            first_payment = booking.total_amount // 2
            second_payment = booking.total_amount - first_payment
            if num_payments == 2:
                amounts = [first_payment, second_payment]
            else:
                third = booking.total_amount // 3
                amounts = [third, third, booking.total_amount - (2 * third)]
        
        for i, amount in enumerate(amounts):
            # Determine payment status based on booking status
            if booking.status == "completed":
                status = "paid"
                paid_at = booking.created_at + timedelta(days=random.randint(0, 3))
            elif booking.status == "confirmed":
                status = "paid" if random.choice([True, False]) else "pending"
                paid_at = booking.created_at + timedelta(days=random.randint(0, 3)) if status == "paid" else None
            elif booking.status == "pending":
                status = "pending"
                paid_at = None
            else:
                status = random.choice(["failed", "refunded"])
                paid_at = booking.created_at + timedelta(days=random.randint(1, 5)) if status == "refunded" else None
            
            payment = Payment(
                booking_id=booking.id,
                reference=f"PYMT{random.randint(100000, 999999)}",
                method=random.choice(payment_methods),
                amount=amount,
                status=status,
                paid_at=paid_at,
                created_at=booking.created_at + timedelta(days=i)  # Stagger payments
            )
            db.session.add(payment)
    
    db.session.commit()

def create_reviews(users, bookings, hostels_with_rooms):
    """Create reviews and ratings"""
    print("⭐ Creating reviews...")
    
    # Only completed bookings get reviews
    completed_bookings = [b for b in bookings if b.status == "completed"]
    
    for booking in completed_bookings:
        # 70% chance of leaving a review
        if random.random() < 0.7:
            # Find the hostel for this booking's room
            hostel_id = None
            for hostel_data in hostels_with_rooms:
                for room in hostel_data["rooms"]:
                    if room.id == booking.room_id:
                        hostel_id = hostel_data["hostel"].id
                        break
                if hostel_id:
                    break
            
            review = Review(
                booking_id=booking.id,
                user_id=booking.student_id,
                hostel_id=hostel_id,
                rating=random.randint(3, 5),  # Mostly positive reviews
                comment=random.choice([
                    "Great place to stay! Very clean and comfortable.",
                    "Good value for money. Would stay again.",
                    "Excellent location near campus.",
                    "Host was very responsive and helpful.",
                    "Quiet environment good for studying.",
                    "Facilities were as described. No issues.",
                    "Minor issues but overall good experience.",
                    "Perfect for students on a budget."
                ]),
                created_at=booking.end_date + timedelta(days=random.randint(1, 7))
            )
            db.session.add(review)
    
    db.session.commit()

def create_wishlists(users, hostels_with_rooms):
    """Create wishlists"""
    print("❤️  Creating wishlists...")
    
    students = [u for u in users if u.role == "student"]
    
    for student in students:
        # Add 1-3 hostels to wishlist
        num_wishlisted = random.randint(1, min(3, len(hostels_with_rooms)))
        selected_hostels = random.sample(hostels_with_rooms, num_wishlisted)
        
        for hostel_data in selected_hostels:
            wishlist = Wishlist(
                user_id=student.id,
                hostel_id=hostel_data["hostel"].id,
                created_at=datetime.now() - timedelta(days=random.randint(1, 30))
            )
            db.session.add(wishlist)
    
    db.session.commit()

def create_notifications(users):
    """Create notifications"""
    print("🔔 Creating notifications...")
    
    notifications_data = [
        "Your booking has been confirmed!",
        "Payment received successfully",
        "New review on your hostel",
        "Booking reminder: Check-in tomorrow",
        "Host verification approved",
        "Welcome to HostelHub!",
        "New message from a host",
        "Special discount available",
        "Maintenance scheduled for this weekend",
        "Your payment is due tomorrow"
    ]
    
    for user in users:
        num_notifications = random.randint(0, 8)
        
        for i in range(num_notifications):
            notification = Notification(
                user_id=user.id,
                title=random.choice(["Booking Update", "Payment", "System", "Message"]),
                message=random.choice(notifications_data),
                is_read=random.choice([True, True, False]),  # 66% read
                created_at=datetime.now() - timedelta(days=random.randint(0, 30))
            )
            db.session.add(notification)
    
    db.session.commit()

def create_room_availability(hostels_with_rooms):
    """Create room availability calendar"""
    print("📆 Creating room availability...")
    
    today = datetime.now().date()
    
    for hostel_data in hostels_with_rooms:
        for room in hostel_data["rooms"]:
            # Create availability for next 90 days
            for day in range(90):
                date = today + timedelta(days=day)
                
                # Determine availability (most days available)
                is_available = random.choice([True, True, True, False])
                
                availability = RoomAvailability(
                    room_id=room.id,
                    date=date,
                    is_available=is_available
                )
                db.session.add(availability)
    
    db.session.commit()

def create_host_earnings(bookings):
    """Create host earnings records"""
    print("💵 Creating host earnings...")
    
    # Filter completed and confirmed bookings
    valid_bookings = [b for b in bookings if b.status in ["completed", "confirmed"]]
    
    for booking in valid_bookings:
        # Get the host ID through room and hostel
        room = Room.query.get(booking.room_id)
        if not room:
            continue
        
        hostel = Hostel.query.get(room.hostel_id)
        if not hostel:
            continue
        
        # Calculate earnings (10% commission)
        commission_rate = 0.10
        commission = int(booking.total_amount * commission_rate)
        net_amount = booking.total_amount - commission
        
        earning = HostEarning(
            host_id=hostel.host_id,
            booking_id=booking.id,
            gross_amount=booking.total_amount,
            commission=commission,
            net_amount=net_amount,
            created_at=booking.created_at + timedelta(days=1)
        )
        db.session.add(earning)
    
    db.session.commit()

def create_support_tickets(users):
    """Create support tickets"""
    print("🎫 Creating support tickets...")
    
    ticket_subjects = [
        "Payment issue",
        "Booking problem",
        "Host verification",
        "Account access",
        "Refund request",
        "Technical issue",
        "Report a problem",
        "General inquiry"
    ]
    
    ticket_messages = [
        "I need help with my payment",
        "My booking status is incorrect",
        "How do I verify my account?",
        "I can't log into my account",
        "Requesting a refund for cancelled booking",
        "The website is not working properly",
        "I want to report inappropriate behavior",
        "Question about your services"
    ]
    
    ticket_statuses = ["open", "in_progress", "resolved", "closed"]
    
    for user in users:
        # 50% chance of creating a ticket
        if random.random() < 0.5:
            ticket = SupportTicket(
                user_id=user.id,
                subject=random.choice(ticket_subjects),
                message=random.choice(ticket_messages),
                status=random.choice(ticket_statuses),
                created_at=datetime.now() - timedelta(days=random.randint(1, 60))
            )
            db.session.add(ticket)
    
    db.session.commit()

def print_summary():
    """Print summary of seeded data"""
    print("\n" + "="*50)
    print("📊 SEEDING SUMMARY")
    print("="*50)
    
    models = [
        ("Users", User),
        ("Tokens", Token),
        ("Hostels", Hostel),
        ("Rooms", Room),
        ("Bookings", Booking),
        ("Payments", Payment),
        ("Reviews", Review),
        ("Wishlists", Wishlist),
        ("Notifications", Notification),
        ("Room Availability", RoomAvailability),
        ("Host Earnings", HostEarning),
        ("Host Verifications", HostVerification),
        ("Support Tickets", SupportTicket),
        ("Settings", Setting)
    ]
    
    for name, model in models:
        try:
            count = db.session.query(model).count()
            print(f"{name}: {count}")
        except:
            print(f"{name}: Error counting")
    
    print("="*50)

# if __name__ == "__main__":
#     # Import your Flask app and initialize it
#     from flask import Flask
#     app = Flask(__name__)
    
#     # Configure your database
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hostelhub.db'  # Change as needed
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
#     db.init_app(app)
    
#     with app.app_context():
#         seed_database()