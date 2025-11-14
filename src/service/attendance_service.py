from src.repository.attendance_repository import AttendanceRepository
from datetime import datetime

class AttendanceService:
    def __init__(self):
        self.attendance_repo = AttendanceRepository()

    def insert_attendance(self, student_id: str, session_id: str):
        attendance_id = str(int(datetime.now().timestamp()))
        attendance_data = {
            "attendance_id": attendance_id,
            "student_id": student_id,
            "session_id": session_id,
            "check_in_time": datetime.now().isoformat(),
            "status": "Present"
        }
        self.attendance_repo.table.insert(attendance_data).execute()
        return attendance_id

    def get_attendance_by_student(self, student_id: str):
        data = self.attendance_repo.table.select("*").eq("student_id", student_id).execute().data
        return data if data else []

    def get_attendance_by_session(self, session_id: str):
        data = self.attendance_repo.table.select("*").eq("session_id", session_id).execute().data
        return data if data else []

    def update_attendance_status(self, attendance_id: str, new_status: str):
        self.attendance_repo.table.update({"status": new_status})\
            .eq("attendance_id", attendance_id).execute()
        return "✅ Đã cập nhật trạng thái điểm danh."
