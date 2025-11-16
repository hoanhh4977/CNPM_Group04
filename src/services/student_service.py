"""
Student Service - Nghiệp vụ của Sinh viên
Chứa tất cả các chức năng mà sinh viên có thể thực hiện
"""

from datetime import datetime
from src.storage.repositories import (
    AttendanceRepository,
    SessionRepository,
    StudentRepository
)
from src.utils.id_generator import generate_attendance_id


class StudentService:
    def __init__(self):
        """Khởi tạo các repository cần thiết"""
        self.attendance_repo = AttendanceRepository()
        self.session_repo = SessionRepository()
        self.student_repo = StudentRepository()

    def mark_attendance(self, student_id: str, session_id: str, attendance_code: str):
        """
        Sinh viên điểm danh bằng mã

        Tham số:
            student_id: Mã sinh viên
            session_id: Mã buổi học
            attendance_code: Mã điểm danh do giảng viên cung cấp

        Trả về:
            dict: {
                "success": True/False,
                "message": "Thông báo kết quả"
            }
        """
        # Bước 1: Kiểm tra xem buổi học có tồn tại không
        from src.storage.client import get_supabase
        session_table = get_supabase().table("session")
        session_data = session_table.select("*").eq("session_id", session_id).execute().data

        if not session_data:
            return {
                "success": False,
                "message": "Không tìm thấy buổi học!"
            }

        session = session_data[0]

        # Bước 2: Kiểm tra mã điểm danh có đúng không
        if session.get("attendance_code") != attendance_code:
            return {
                "success": False,
                "message": "Mã điểm danh không đúng!"
            }

        # Bước 3: Kiểm tra xem sinh viên đã điểm danh chưa
        existing = self.attendance_repo.table.select("*")\
            .eq("student_id", student_id)\
            .eq("session_id", session_id)\
            .execute().data

        if existing:
            return {
                "success": False,
                "message": "Bạn đã điểm danh buổi học này rồi!"
            }

        # Bước 4: Tạo bản ghi điểm danh
        attendance_id = generate_attendance_id()
        attendance_data = {
            "attendance_id": attendance_id,
            "student_id": student_id,
            "session_id": session_id,
            "status": "present",
            "check_in_time": datetime.now().isoformat()
        }

        try:
            self.attendance_repo.create(attendance_data)
            return {
                "success": True,
                "message": "Điểm danh thành công!",
                "data": {
                    "subject_name": session.get("subject_name"),
                    "session_date": session.get("session_date"),
                    "time_slot": session.get("time_slot")
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi khi điểm danh: {str(e)}"
            }

    def get_my_sessions(self, student_id: str):
        """
        Xem danh sách các buổi học đã điểm danh

        Tham số:
            student_id: Mã sinh viên

        Trả về:
            list: Danh sách các buổi học
        """
        return self.session_repo.get_sessions_for_student(student_id)

    def get_my_attendance_history(self, student_id: str):
        """
        Xem lịch sử điểm danh của bản thân

        Tham số:
            student_id: Mã sinh viên

        Trả về:
            list: Danh sách điểm danh kèm thông tin buổi học
        """
        # Lấy tất cả attendance records của sinh viên
        attendances = self.attendance_repo.get_by_student(student_id)

        if not attendances:
            return []

        # Lấy thông tin session cho mỗi attendance
        from src.storage.client import get_supabase
        session_table = get_supabase().table("session")

        result = []
        for att in attendances:
            session_id = att.get("session_id")
            session_data = session_table.select("*").eq("session_id", session_id).execute().data

            if session_data:
                session = session_data[0]
                result.append({
                    "attendance_id": att.get("attendance_id"),
                    "session_id": session_id,
                    "subject_name": session.get("subject_name"),
                    "session_date": session.get("session_date"),
                    "time_slot": session.get("time_slot"),
                    "status": att.get("status"),
                    "check_in_time": att.get("check_in_time")
                })

        return result

    def get_announcements(self, scope: str = "student"):
        """
        Xem thông báo dành cho sinh viên

        Tham số:
            scope: Phạm vi thông báo (student hoặc all)

        Trả về:
            list: Danh sách thông báo
        """
        from src.storage.client import get_supabase
        notification_table = get_supabase().table("notification")

        # Lấy thông báo có scope = 'student' hoặc 'all'
        notifications = notification_table.select("*")\
            .in_("scope", ["student", "all"])\
            .order("creation_date", desc=True)\
            .execute().data

        return notifications if notifications else []
