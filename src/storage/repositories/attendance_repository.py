from src.storage.client import get_supabase

class AttendanceRepository:
    def __init__(self):
        self.db = get_supabase()
        self.table = self.db.table("attendance")

    def get_by_student(self, student_id):
        return self.table.select("*").eq("student_id", student_id).execute().data or []

    def get_attendance(self, student_id, session_id):
        return self.table.select("*")\
            .eq("student_id", student_id)\
            .eq("session_id", session_id)\
            .execute().data

    def create_attendance(self, attendance_data):
        return self.table.insert(attendance_data).execute().data

    def update_attendance(self, student_id, session_id, update_data):
        return self.table.update(update_data)\
            .eq("student_id", student_id)\
            .eq("session_id", session_id)\
            .execute().data

    def delete_attendance(self, student_id, session_id):
        return self.table.delete()\
            .eq("student_id", student_id)\
            .eq("session_id", session_id)\
            .execute().data
    def get_by_session(self, session_id):
        return self.table.select("*").eq("session_id", session_id).execute().data
    def update_status(self, attendance_id, new_status):
        return self.table.update({"status": new_status}).eq("attendance_id", attendance_id).execute().data

