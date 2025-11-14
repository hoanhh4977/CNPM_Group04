from src.storage.client import get_supabase

class AttendanceRepository:
    def __init__(self):
        self.db = get_supabase()
        self.table = self.db.table("attendance")
