from flask import Blueprint
from flask_restful import Api
from .students import StudentDashboard, StudentBookingList

student_bp = Blueprint('student', __name__)
student_api = Api(student_bp)
student_api.add_resource(StudentDashboard, '/dashboard-stats')
student_api.add_resource(StudentBookingList, '/bookings')