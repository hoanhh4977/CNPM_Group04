import uuid
from datetime import date
from src.repository.attendance_repository import AttendanceRepository

class AttendanceService:
    def __init__(self):
        self.attendance_repository = AttendanceRepository()

    def get_attendance(self, student_id, session_id):
        return self.attendance_repository.get_attendance(student_id, session_id)

    def create_attendance(self, student_id, session_id, status):
        attendance_id = uuid.uuid4().int % 1000000
        attendance_data = {
            "student_id": student_id,
            "session_id": session_id,
            "status": status
        }
        return self.attendance_repository.create_attendance(attendance_data)

    def update_attendance(self, student_id, session_id, status):
        update_data = {
            "status": status
        }
        return self.attendance_repository.update_attendance(student_id, session_id, update_data)

    def delete_attendance(self, student_id, session_id):
        return self.attendance_repository.delete_attendance(student_id, session_id)
