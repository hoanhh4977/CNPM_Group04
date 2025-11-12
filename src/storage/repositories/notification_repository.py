from src.storage.client import get_supabase

class NotificationRepository:
    def __init__(self):
        self.db = get_supabase()
        self.table = self.db.table("notification")