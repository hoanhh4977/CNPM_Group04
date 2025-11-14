from src.repository.student_repository import StudentRepository
from src.repository.attendance_repository import AttendanceRepository
from src.repository.session_repository import SessionRepository
from datetime import datetime

class StudentService:
    def __init__(self):
        self.student_repo = StudentRepository()
        self.attendance_repo = AttendanceRepository()
        self.session_repo = SessionRepository()

    def view_upcoming_sessions(self):
        today = datetime.today().date().isoformat()
        sessions = self.session_repo.table.select("*").gte("session_date", today).execute().data
        return sessions if sessions else []

    def mark_attendance(self, student_id: str, session_id: str, code_input: str):
        session = self.session_repo.table.select("*")\
            .eq("session_id", session_id)\
            .eq("attendance_code", code_input)\
            .execute().data

        if session:
            attendance_id = str(int(datetime.now().timestamp()))
            self.attendance_repo.table.insert({
                "attendance_id": attendance_id,
                "student_id": student_id,
                "session_id": session_id,
                "check_in_time": datetime.now().isoformat(),
                "status": "Present"
            }).execute()
            return "✅ Điểm danh thành công!"
        else:
            return "❌ Mã điểm danh không hợp lệ."

    def view_attendance_results(self, student_id: str):
        results = self.attendance_repo.table.select("*").eq("student_id", student_id).execute().data
        return results if results else []
