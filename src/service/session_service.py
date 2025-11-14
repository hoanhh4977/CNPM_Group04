from src.repository.session_repository import SessionRepository
from datetime import date

class SessionService:
    def __init__(self):
        self.session_repo = SessionRepository()

    def get_upcoming_sessions(self):
        return self.session_repo.get_upcoming().data

    def get_sessions_by_lecturer(self, lecturer_id):
        return self.session_repo.get_by_lecturer(lecturer_id).data

    def get_session_by_code(self, session_id, attendance_code):
        return self.session_repo.get_by_code(session_id, attendance_code).data

    def create_session(self, lecturer_id, subject_name, time_slot, attendance_code=None):
        session_id = str(hash(subject_name + time_slot + lecturer_id) % 100000)
        if attendance_code is None:
            from utils import generate_attendance_code
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
        return session_id, attendance_code