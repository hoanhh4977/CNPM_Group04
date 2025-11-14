from src.repository.session_repository import SessionRepository

class SessionService:
    def __init__(self):
        self.session_repo = SessionRepository()

    def get_sessions_by_lecturer(self, lecturer_id: str):
        data = self.session_repo.table.select("*").eq("lecturer_id", lecturer_id).execute().data
        return data if data else []

    def get_session_by_id(self, session_id: str):
        data = self.session_repo.table.select("*").eq("session_id", session_id).execute().data
        return data[0] if data else None
