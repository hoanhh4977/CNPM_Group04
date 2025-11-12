from src.storage.client import get_supabase

class AdminRepository:
    def __init__(self):
        self.db = get_supabase()
        self.table = self.db.table("administrator")