from src.repository.session_repository import SessionRepository

class SessionService:
    def __init__(self):
        self.session_repo = SessionRepository()

    def get_sessions_for_student(self, student_id):
        return self.session_repo.get_sessions_for_student(student_id)
