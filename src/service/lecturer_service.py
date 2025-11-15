import uuid
import random
import string
from datetime import date
from src.repository.lecturer_repository import LecturerRepository
from src.repository.session_repository import SessionRepository
from src.repository.attendance_repository import AttendanceRepository
from src.storage.client import get_supabase

class LecturerService:
    def __init__(self):
        self.lecturer_repo = LecturerRepository()
        self.session_repo = SessionRepository()
        self.attendance_repo = AttendanceRepository()
        self.attendance_table = get_supabase().table("attendance")
    


    def view_attendance_by_session(self, session_id):
        return self.attendance_table \
            .select("student_id, status") \
            .eq("session_id", session_id) \
            .execute().data or []

    
    def generate_lecturer_id(self):
        return "L" + str(uuid.uuid4().int % 10000).zfill(4)  # Ví dụ: L1234

    def generate_session_id(self):
        return str(uuid.uuid4().int % 100000).zfill(5)  # Ví dụ: 04237

    def generate_attendance_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))  # Ví dụ: A7X3B

    def ensure_lecturer_exists(self, lecturer_id):
        if not self.lecturer_repo.get_by_id(lecturer_id):
            self.lecturer_repo.create({
                "lecturer_id": lecturer_id
            })

    def create_session(self, subject_name=None, time_slot=None):
        lecturer_id = self.generate_lecturer_id()
        self.ensure_lecturer_exists(lecturer_id)

        session_id = self.generate_session_id()
        attendance_code = self.generate_attendance_code()
        session_data = {
            "session_id": session_id,
            "lecturer_id": lecturer_id,
            "session_date": date.today().isoformat(),
            "time_slot": time_slot,
            "subject_name": subject_name,
            "attendance_code": attendance_code
        }
        self.session_repo.create(session_data)
        return session_data
    from src.storage.client import get_supabase

class LecturerService:
    def __init__(self):
        self.attendance_table = get_supabase().table("attendance")

    def update_attendance_status_by_student(self, student_id, session_id, new_status):
        result = self.attendance_table \
            .update({"status": new_status}) \
            .eq("student_id", student_id) \
            .eq("session_id", session_id) \
            .execute().data

        if result:
            return " Cập nhật trạng thái thành công!"
        else:
            return " Không tìm thấy bản ghi điểm danh để cập nhật."
