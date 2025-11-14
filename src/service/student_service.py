from datetime import datetime
from src.repository.attendance_repository import AttendanceRepository
from src.repository.session_repository import SessionRepository
from src.repository.student_repository import StudentRepository

class StudentService:
    def __init__(self):
        self.attendance_repo = AttendanceRepository()
        self.session_repo = SessionRepository()
        self.student_repo = StudentRepository()

    def mark_attendance(self, student_id, session_id, code_input):
        session = self.session_repo.get_by_code(session_id, code_input)
        if session.data:
            attendance_id = str(int(datetime.now().timestamp()))
            data = {
                "attendance_id": attendance_id,
                "student_id": student_id,
                "session_id": session_id,
                "check_in_time": datetime.now().isoformat(),
                "status": "Present"
            }
            self.attendance_repo.insert_attendance(data)
            return "✅ Điểm danh thành công!"
        else:
            return "❌ Mã điểm danh không hợp lệ."

    def view_attendance_results(self, student_id):
        results = self.attendance_repo.get_by_student(student_id)
        return results.data

    def get_students_by_class(self, class_name):
        return self.student_repo.get_students_by_class(class_name).data