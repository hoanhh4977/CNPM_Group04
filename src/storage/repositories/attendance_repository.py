from src.storage.client import get_supabase

class AttendanceRepository:
    def __init__(self):
        self.db = get_supabase()
        self.table = self.db.table("attendance")

    def create(self, data):
        return self.table.insert(data).execute().data

    def get_by_student(self, student_id):
        return self.table.select("*").eq("student_id", student_id).execute().data or []

    def get_by_session(self, session_id):
        return self.table.select("*").eq("session_id", session_id).execute().data or []

    def update_attendance(self, student_id, session_id, update_data):
        return self.table.update(update_data)\
            .eq("student_id", student_id)\
            .eq("session_id", session_id)\
            .execute().data

    def update_status(self, attendance_id, new_status):
        return self.table.update({"status": new_status})\
            .eq("attendance_id", attendance_id)\
            .execute().data

    def delete_attendance_by_id(self, attendance_id):
        return self.table.delete().eq("attendance_id", attendance_id).execute().data
    
