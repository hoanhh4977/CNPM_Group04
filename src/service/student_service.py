import uuid
from src.repository.attendance_repository import AttendanceRepository
from src.storage.client import get_supabase

class StudentService:
    def __init__(self):
        self.attendance_repo = AttendanceRepository()
        self.student_table = get_supabase().table("student")
        self.session_table = get_supabase().table("session")

    def generate_attendance_id(self):
        return str(uuid.uuid4().int % 100000).zfill(5)  # Ví dụ: "04237"

    def ensure_student_exists(self, student_id):
        existing = self.student_table.select("*").eq("student_id", student_id).execute().data
        if not existing:
            self.student_table.insert({
                "student_id": student_id
            }).execute()

    def mark_attendance(self, student_id, session_id, attendance_code):
        # Kiểm tra mã điểm danh
        session_data = self.session_table.select("attendance_code").eq("session_id", session_id).execute().data
        if not session_data or session_data[0]["attendance_code"] != attendance_code:
            return " Mã điểm danh không đúng."

        # Đảm bảo sinh viên tồn tại
        self.ensure_student_exists(student_id)

        # Tạo mã điểm danh
        attendance_id = self.generate_attendance_id()

        # Ghi nhận điểm danh
        self.attendance_repo.create({
            "attendance_id": attendance_id,
            "student_id": student_id,
            "session_id": session_id,
            "status": "present"
        })

        return " Điểm danh thành công!"
