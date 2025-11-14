from datetime import datetime
from src.repository.attendance_repository import AttendanceRepository

class AttendanceService:
    def __init__(self):
        self.attendance_repo = AttendanceRepository()

    def insert_attendance(self, student_id, session_id):
        attendance_id = str(int(datetime.now().timestamp()))
        data = {
            "attendance_id": attendance_id,
            "student_id": student_id,
            "session_id": session_id,
            "check_in_time": datetime.now().isoformat(),
            "status": "Present"
        }
        self.attendance_repo.insert_attendance(data)
        return attendance_id

    def get_attendance_by_student(self, student_id):
        return self.attendance_repo.get_by_student(student_id).data

    def get_attendance_by_session(self, session_id):
        return self.attendance_repo.get_by_session(session_id).data

    def update_attendance_status(self, attendance_id, new_status):
        self.attendance_repo.update_status(attendance_id, new_status)
        return "✅ Đã cập nhật trạng thái điểm danh."