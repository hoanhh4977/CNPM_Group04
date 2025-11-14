from src.repository.lecturer_repository import LecturerRepository
from src.repository.session_repository import SessionRepository
from src.repository.attendance_repository import AttendanceRepository
from utils import generate_attendance_code
from datetime import date

class LecturerService:
    def __init__(self):
        self.lecturer_repo = LecturerRepository()
        self.session_repo = SessionRepository()
        self.attendance_repo = AttendanceRepository()

    def create_session(self, lecturer_id: str, subject_name: str, time_slot: str):
        session_id = str(hash(subject_name + time_slot + lecturer_id) % 100000)
        attendance_code = generate_attendance_code()

        self.session_repo.table.insert({
            "session_id": session_id,
            "lecturer_id": lecturer_id,
            "session_date": date.today().isoformat(),
            "time_slot": time_slot,
            "subject_name": subject_name,
            "attendance_code": attendance_code
        }).execute()

        return session_id, attendance_code

    def view_class_attendance(self, session_id: str):
        results = self.attendance_repo.table.select("*").eq("session_id", session_id).execute().data
        return results if results else []

    def edit_attendance(self, attendance_id: str, new_status: str):
        self.attendance_repo.table.update({"status": new_status})\
            .eq("attendance_id", attendance_id).execute()
        return "✅ Đã cập nhật trạng thái điểm danh."
