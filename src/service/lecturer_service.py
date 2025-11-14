from datetime import date
from src.repository.attendance_repository import AttendanceRepository
from src.repository.session_repository import SessionRepository
from src.repository.lecturer_repository import LecturerRepository
from utils import generate_attendance_code

class LecturerService:
    def __init__(self):
        self.attendance_repo = AttendanceRepository()
        self.session_repo = SessionRepository()
        self.lecturer_repo = LecturerRepository()

    def create_session(self, lecturer_id, subject_name, time_slot):
        session_id = str(hash(subject_name + time_slot + lecturer_id) % 100000)
        attendance_code = generate_attendance_code()
        data = {
            "session_id": session_id,
            "lecturer_id": lecturer_id,
            "session_date": date.today().isoformat(),
            "time_slot": time_slot,
            "subject_name": subject_name,
            "attendance_code": attendance_code
        }
        self.session_repo.create_session(data)
        return attendance_code

    def view_class_attendance(self, session_id):
        return self.attendance_repo.get_by_session(session_id).data

    def edit_attendance(self, attendance_id, new_status):
        self.attendance_repo.update_status(attendance_id, new_status)
        return "✅ Đã cập nhật trạng thái điểm danh."

    def get_lecturer_info(self, lecturer_id):
        return self.lecturer_repo.get_lecturer_by_id(lecturer_id).data
