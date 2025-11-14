from supabase_client import supabase

class SessionRepository:
    def get_by_code(self, session_id, code):
        return supabase.table("session").select("*").eq("session_id", session_id).eq("attendance_code", code).execute()

    def get_upcoming(self):
        from datetime import date
        today = date.today().isoformat()
        return supabase.table("session").select("*").gte("session_date", today).execute()

    def create_session(self, data):
        return supabase.table("session").insert(data).execute()
