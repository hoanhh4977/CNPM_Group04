from src.repository.attendance_repository import AttendanceRepository

class AttendanceService:
    def __init__(self):
        self.attendance_repo = AttendanceRepository()

    def delete_attendance_by_id(self, attendance_id):
        return self.attendance_repo.delete_attendance_by_id(attendance_id)
