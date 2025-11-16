"""
Lecturer Service - Nghiệp vụ của Giảng viên
Chứa tất cả các chức năng mà giảng viên có thể thực hiện
"""

from datetime import date, datetime
import pytz
from utils import generate_attendance_code
from src.storage.repositories import (
    AttendanceRepository,
    SessionRepository,
    LecturerRepository
)
from src.utils.id_generator import generate_session_id, generate_notification_id


class LecturerService:
    def __init__(self):
        """Khởi tạo các repository cần thiết"""
        self.attendance_repo = AttendanceRepository()
        self.session_repo = SessionRepository()
        self.lecturer_repo = LecturerRepository()

    def create_session(self, lecturer_id: str, subject_name: str, time_slot: str):
        """
        Tạo buổi học mới

        Tham số:
            lecturer_id: Mã giảng viên
            subject_name: Tên môn học
            time_slot: Ca học (Sáng/Chiều/Tối)

        Trả về:
            dict: {
                "success": True/False,
                "message": "Thông báo",
                "data": {...} # Thông tin buổi học nếu thành công
            }
        """
        # Tạo mã buổi học và mã điểm danh
        session_id = generate_session_id()
        attendance_code = generate_attendance_code()

        session_data = {
            "session_id": session_id,
            "lecturer_id": lecturer_id,
            "session_date": date.today().isoformat(),
            "time_slot": time_slot,
            "subject_name": subject_name,
            "attendance_code": attendance_code
        }

        try:
            result = self.session_repo.create(session_data)
            return {
                "success": True,
                "message": "Tạo buổi học thành công!",
                "data": session_data
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi khi tạo buổi học: {str(e)}"
            }

    def get_my_sessions(self, lecturer_id: str):
        """
        Xem tất cả buổi học của giảng viên

        Tham số:
            lecturer_id: Mã giảng viên

        Trả về:
            list: Danh sách buổi học
        """
        from src.storage.client import get_supabase
        session_table = get_supabase().table("session")

        sessions = session_table.select("*")\
            .eq("lecturer_id", lecturer_id)\
            .order("session_date", desc=True)\
            .execute().data

        return sessions if sessions else []

    def view_attendance_by_session(self, session_id: str):
        """
        Xem danh sách điểm danh theo buổi học

        Tham số:
            session_id: Mã buổi học

        Trả về:
            list: Danh sách sinh viên đã điểm danh kèm thông tin
        """
        # Lấy attendance records
        attendances = self.attendance_repo.get_by_session(session_id)

        if not attendances:
            return []

        # Lấy thông tin sinh viên cho mỗi attendance
        from src.storage.client import get_supabase
        student_table = get_supabase().table("student")
        user_table = get_supabase().table("User")

        result = []
        for att in attendances:
            student_id = att.get("student_id")

            # Lấy thông tin student
            student_data = student_table.select("*").eq("student_id", student_id).execute().data
            if student_data:
                student = student_data[0]
                user_id = student.get("user_id")

                # Lấy thông tin user (tên, ...)
                user_data = user_table.select("*").eq("user_id", user_id).execute().data
                if user_data:
                    user = user_data[0]
                    result.append({
                        "attendance_id": att.get("attendance_id"),
                        "student_id": student_id,
                        "student_name": user.get("full_name"),
                        "class_name": student.get("class_name"),
                        "status": att.get("status"),
                        "check_in_time": att.get("check_in_time")
                    })

        return result

    def update_attendance_status(self, attendance_id: str, new_status: str):
        """
        Cập nhật trạng thái điểm danh

        Tham số:
            attendance_id: Mã điểm danh
            new_status: Trạng thái mới (present/absent/late)

        Trả về:
            dict: {
                "success": True/False,
                "message": "Thông báo"
            }
        """
        try:
            result = self.attendance_repo.update_status(attendance_id, new_status)
            if result:
                return {
                    "success": True,
                    "message": f"Đã cập nhật trạng thái thành '{new_status}'"
                }
            else:
                return {
                    "success": False,
                    "message": "Không tìm thấy bản ghi điểm danh!"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi khi cập nhật: {str(e)}"
            }

    def get_session_statistics(self, session_id: str):
        """
        Xem thống kê điểm danh theo buổi học

        Tham số:
            session_id: Mã buổi học

        Trả về:
            dict: Thống kê số lượng present/absent/late
        """
        attendances = self.attendance_repo.get_by_session(session_id)

        stats = {
            "total": len(attendances),
            "present": 0,
            "absent": 0,
            "late": 0
        }

        for att in attendances:
            status = att.get("status", "").lower()
            if status in stats:
                stats[status] += 1

        return stats

    def create_announcement(self, lecturer_id: str, content: str, scope: str = "student"):
        """
        Tạo thông báo

        Tham số:
            lecturer_id: Mã giảng viên (creator)
            content: Nội dung thông báo
            scope: Phạm vi (all/student/lecturer)

        Trả về:
            dict: {
                "success": True/False,
                "message": "Thông báo"
            }
        """
        # Lấy user_id từ lecturer_id
        lecturer = self.lecturer_repo.get_by_id(lecturer_id)
        if not lecturer:
            return {
                "success": False,
                "message": "Không tìm thấy thông tin giảng viên!"
            }

        creator_id = lecturer.get("user_id")

        # Tạo thông báo
        from src.storage.client import get_supabase
        notification_table = get_supabase().table("notification")

        VN_TIMEZONE = pytz.timezone("Asia/Ho_Chi_Minh")
        notification_data = {
            "notification_id": generate_notification_id(),
            "creator_id": creator_id,
            "content": content,
            "scope": scope,
            "creation_date": datetime.now(VN_TIMEZONE).isoformat()
        }

        try:
            notification_table.insert(notification_data).execute()
            return {
                "success": True,
                "message": "Tạo thông báo thành công!"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi khi tạo thông báo: {str(e)}"
            }

    def get_announcements(self):
        """
        Xem tất cả thông báo

        Trả về:
            list: Danh sách thông báo
        """
        from src.storage.client import get_supabase
        notification_table = get_supabase().table("notification")

        # Lấy thông báo có scope = 'lecturer' hoặc 'all'
        notifications = notification_table.select("*")\
            .in_("scope", ["lecturer", "all"])\
            .order("creation_date", desc=True)\
            .execute().data

        return notifications if notifications else []
