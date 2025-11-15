import uuid
from datetime import date
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

    def get_lecturer_info(self, lecturer_id):
        return self.lecturer_repo.get_by_id(lecturer_id)

    def create_session(self, lecturer_id, subject_name, time_slot):
        session_id = str(hash(subject_name + time_slot + lecturer_id) % 100000)
        attendance_code = generate_attendance_code()
        session_data = {
            "session_id": session_id,
            "lecturer_id": lecturer_id,
            "session_date": date.today().isoformat(),
            "time_slot": time_slot,
            "subject_name": subject_name,
            "attendance_code": attendance_code
        }
        return self.session_repo.create(session_data)

    def view_attendance_by_session(self, session_id):
        return self.attendance_repo.get_by_session(session_id)

    def update_attendance_status(self, attendance_id, new_status):
        return self.attendance_repo.update_status(attendance_id, new_status)
    
