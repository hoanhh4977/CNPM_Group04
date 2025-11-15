from src.storage.client import get_supabase

class SessionRepository:
    def __init__(self):
        self.session_table = get_supabase().table("session")
        self.attendance_table = get_supabase().table("attendance")

    def get_sessions_for_student(self, student_id):
        # lấy danh sách session_id từ bảng attendance
        attendance_records = self.attendance_table \
            .select("session_id") \
            .eq("student_id", student_id) \
            .execute().data or []

        session_ids = [record["session_id"] for record in attendance_records]

        if not session_ids:
            return []

        # truy vấn bảng session theo danh sách session_id
        return self.session_table \
            .select("*") \
            .in_("session_id", session_ids) \
            .execute().data or []

