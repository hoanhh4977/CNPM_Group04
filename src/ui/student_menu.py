"""
Student Menu - Menu dành cho Sinh viên
"""

from src.services.student_service import StudentService
from src.utils.formatters import (
    print_header, print_menu, print_section, print_table,
    print_success, print_error, print_info, format_date, format_datetime
)
from src.ui.helpers import get_input, pause


class StudentMenu:
    def __init__(self, user_data: dict):
        """
        Khởi tạo Student Menu

        Tham số:
            user_data: Dict chứa thông tin user đã đăng nhập
                {
                    "user_id": "...",
                    "full_name": "...",
                    "student_id": "...",
                    ...
                }
        """
        self.user_data = user_data
        self.student_id = user_data.get("student_id")
        self.full_name = user_data.get("full_name")
        self.service = StudentService()

    def run(self):
        """Chạy menu sinh viên"""
        while True:
            print_header(f"MENU SINH VIÊN - {self.full_name}")
            print(f"  Mã sinh viên: {self.student_id}\n")

            print_menu("CHỨC NĂNG", [
                ("1", "Điểm danh"),
                ("2", "Xem lịch học"),
                ("3", "Xem lịch sử điểm danh"),
                ("4", "Xem thông báo"),
                ("0", "Đăng xuất")
            ], show_back=False)

            choice = get_input("Lựa chọn của bạn")

            if choice == "1":
                self.mark_attendance()
            elif choice == "2":
                self.view_schedule()
            elif choice == "3":
                self.view_attendance_history()
            elif choice == "4":
                self.view_announcements()
            elif choice == "0":
                print_success("Đăng xuất thành công!")
                break
            else:
                print_error("Lựa chọn không hợp lệ!")
                pause()

    def mark_attendance(self):
        """Điểm danh"""
        print_section("ĐIỂM DANH")

        session_id = get_input("Nhập mã buổi học")
        attendance_code = get_input("Nhập mã điểm danh")

        result = self.service.mark_attendance(
            student_id=self.student_id,
            session_id=session_id,
            attendance_code=attendance_code
        )

        if result["success"]:
            print_success(result["message"])
            if "data" in result:
                data = result["data"]
                print(f"\n  📚 Môn học: {data.get('subject_name')}")
                print(f"  📅 Ngày: {format_date(data.get('session_date'))}")
                print(f"  ⏰ Ca: {data.get('time_slot')}")
        else:
            print_error(result["message"])

        pause()

    def view_schedule(self):
        """Xem lịch học (các buổi đã điểm danh)"""
        print_section("LỊCH HỌC CỦA TÔI")

        sessions = self.service.get_my_sessions(self.student_id)

        if not sessions:
            print_info("Bạn chưa điểm danh buổi học nào.")
            pause()
            return

        # Chuẩn bị dữ liệu cho bảng
        headers = ["STT", "Môn học", "Ngày", "Ca học", "Mã buổi"]
        rows = []

        for i, session in enumerate(sessions, 1):
            rows.append([
                str(i),
                session.get("subject_name", "N/A"),
                format_date(session.get("session_date", "")),
                session.get("time_slot", "N/A"),
                session.get("session_id", "N/A")
            ])

        print_table(headers, rows)
        print(f"\n  Tổng số: {len(sessions)} buổi học")
        pause()

    def view_attendance_history(self):
        """Xem lịch sử điểm danh"""
        print_section("LỊCH SỬ ĐIỂM DANH")

        history = self.service.get_my_attendance_history(self.student_id)

        if not history:
            print_info("Chưa có lịch sử điểm danh.")
            pause()
            return

        # Chuẩn bị dữ liệu cho bảng
        headers = ["STT", "Môn học", "Ngày", "Ca", "Trạng thái", "Thời gian điểm danh"]
        rows = []

        # Đếm số lượng theo trạng thái
        stats = {"present": 0, "absent": 0, "late": 0}

        for i, record in enumerate(history, 1):
            status = record.get("status", "").lower()
            if status in stats:
                stats[status] += 1

            # Icon cho trạng thái
            status_display = {
                "present": "✅ Có mặt",
                "absent": "❌ Vắng",
                "late": "⏰ Muộn"
            }.get(status, status)

            rows.append([
                str(i),
                record.get("subject_name", "N/A"),
                format_date(record.get("session_date", "")),
                record.get("time_slot", "N/A"),
                status_display,
                format_datetime(record.get("check_in_time", ""))
            ])

        print_table(headers, rows)

        # Hiển thị thống kê
        print(f"\n  📊 THỐNG KÊ:")
        print(f"  - Tổng số buổi: {len(history)}")
        print(f"  - Có mặt: {stats['present']} buổi")
        print(f"  - Vắng: {stats['absent']} buổi")
        print(f"  - Đi muộn: {stats['late']} buổi")

        if len(history) > 0:
            attendance_rate = (stats['present'] / len(history)) * 100
            print(f"  - Tỷ lệ tham gia: {attendance_rate:.1f}%")

        pause()

    def view_announcements(self):
        """Xem thông báo"""
        print_section("THÔNG BÁO")

        announcements = self.service.get_announcements()

        if not announcements:
            print_info("Chưa có thông báo nào.")
            pause()
            return

        for i, announcement in enumerate(announcements, 1):
            scope = announcement.get("scope", "")
            scope_display = {
                "all": "📢 [TẤT CẢ]",
                "student": "🎓 [SINH VIÊN]",
                "lecturer": "👨‍🏫 [GIẢNG VIÊN]"
            }.get(scope, scope)

            print(f"\n  {i}. {scope_display}")
            print(f"     📅 {format_datetime(announcement.get('creation_date', ''))}")
            print(f"     📝 {announcement.get('content', '')}")
            print("     " + "-" * 50)

        print(f"\n  Tổng số: {len(announcements)} thông báo")
        pause()
