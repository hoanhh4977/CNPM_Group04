from src.storage.client import get_supabase

class SessionRepository:
    def __init__(self):
        self.db = get_supabase()
        self.table = self.db.table("session")
    def create(self, session_data):
        return self.table.insert(session_data).execute().data

    def get_by_id(self, session_id):
        return self.table.select("*").eq("session_id", session_id).execute().data or []


    def get_by_lecturer(self, lecturer_id):
        return self.table.select("*").eq("lecturer_id", lecturer_id).execute().data or []
