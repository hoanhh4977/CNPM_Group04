import uuid
from datetime import date
from src.repository.student_repository import StudentRepository
from src.repository.attendance_repository import AttendanceRepository
from src.repository.session_repository import SessionRepository

class StudentService:
    def __init__(self):
        self.student_repo = StudentRepository()
        self.attendance_repo = AttendanceRepository()
        self.session_repo = SessionRepository()

    def get_student_info(self, student_id):
        return self.student_repo.get_by_id(student_id)

    def view_attendance(self, student_id):
        return self.attendance_repo.get_by_student(student_id)

    def register_student(self, student_data):
        return self.student_repo.create(student_data)

    def update_student(self, student_id, update_data):
        return self.student_repo.update(student_id, update_data)

    def delete_student(self, student_id):
        return self.student_repo.delete(student_id)

    def mark_attendance(self, student_id, session_id, attendance_code):
        session_list = self.session_repo.get_by_id(session_id)

        if not isinstance(session_list, list) or len(session_list) == 0:
            return "❌ Không tìm thấy buổi học!"

        session = session_list[0]

        if session.get("attendance_code") != attendance_code:
            return "❌ Mã điểm danh không hợp lệ."

        attendance_id = uuid.uuid4().int % 1000000
        attendance_data = {
            "attendance_id": attendance_id,
            "student_id": student_id,
            "session_id": session_id,
            "status": "Present"
        }

        self.attendance_repo.create_attendance(attendance_data)
        return "✅ Điểm danh thành công!"
