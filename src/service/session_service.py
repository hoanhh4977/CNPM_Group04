import uuid
from datetime import date
from src.storage.repositories.session_repository import SessionRepository

class SessionService:
    def __init__(self):
        self.session_repo = SessionRepository()

    def get_session_info(self, session_id):
        return self.session_repo.get_by_id(session_id)

    def get_sessions_for_lecturer(self, lecturer_id):
        return self.session_repo.get_by_lecturer(lecturer_id)
    def create_session(self, lecturer_id, subject_name, time_slot):
        session_id = uuid.uuid4().int % 1000000
        attendance_code = str(uuid.uuid4().int)[:5]

        session_data = {
            "session_id": session_id,
            "lecturer_id": lecturer_id,
            "session_date": date.today().isoformat(),
            "time_slot": time_slot,
            "subject_name": subject_name,
            "attendance_code": attendance_code
        }

        return self.session_repo.create(session_data)
