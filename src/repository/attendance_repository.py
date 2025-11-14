from supabase_client import supabase

class AttendanceRepository:
    def insert_attendance(self, data):
        return supabase.table("attendance").insert(data).execute()

    def get_by_student(self, student_id):
        return supabase.table("attendance").select("*").eq("student_id", student_id).execute()

    def get_by_session(self, session_id):
        return supabase.table("attendance").select("*").eq("session_id", session_id).execute()

    def update_status(self, attendance_id, new_status):
        return supabase.table("attendance").update({"status": new_status}).eq("attendance_id", attendance_id).execute()