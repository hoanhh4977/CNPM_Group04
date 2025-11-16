"""
Lecturer Menu - Menu dành cho Giảng viên
"""

from src.services.lecturer_service import LecturerService
from src.utils.formatters import (
    print_header, print_menu, print_section, print_table,
    print_success, print_error, print_info, print_warning,
    format_date, format_datetime
)
from src.ui.helpers import get_input, get_choice, pause, confirm_action


class LecturerMenu:
    def __init__(self, user_data: dict):
        """
        Khởi tạo Lecturer Menu

        Tham số:
            user_data: Dict chứa thông tin user đã đăng nhập
        """
        self.user_data = user_data
        self.lecturer_id = user_data.get("lecturer_id")
        self.full_name = user_data.get("full_name")
        self.service = LecturerService()

    def run(self):
        """Chạy menu giảng viên"""
        while True:
            print_header(f"MENU GIẢNG VIÊN - {self.full_name}")
            print(f"  Mã giảng viên: {self.lecturer_id}\n")

            print_menu("CHỨC NĂNG", [
                ("1", "Tạo buổi học mới"),
                ("2", "Xem danh sách buổi học của tôi"),
                ("3", "Xem điểm danh theo buổi"),
                ("4", "Cập nhật trạng thái điểm danh"),
                ("5", "Thống kê điểm danh"),
                ("6", "Tạo thông báo"),
                ("7", "Xem thông báo"),
                ("0", "Đăng xuất")
            ], show_back=False)

            choice = get_input("Lựa chọn của bạn")

            if choice == "1":
                self.create_session()
            elif choice == "2":
                self.view_my_sessions()
            elif choice == "3":
                self.view_attendance()
            elif choice == "4":
                self.update_attendance_status()
            elif choice == "5":
                self.view_statistics()
            elif choice == "6":
                self.create_announcement()
            elif choice == "7":
                self.view_announcements()
            elif choice == "0":
                print_success("Đăng xuất thành công!")
                break
            else:
                print_error("Lựa chọn không hợp lệ!")
                pause()

    def create_session(self):
        """Tạo buổi học mới"""
        print_section("TẠO BUỔI HỌC MỚI")

        subject_name = get_input("Tên môn học")

        # Validate subject name length
        if len(subject_name) > 100:
            print_error("Tên môn học quá dài! Vui lòng nhập tối đa 100 ký tự.")
            pause()
            return

        print("\n  Chọn ca học:")
        print("  1. Sáng (7:00 - 11:00)")
        print("  2. Chiều (13:00 - 17:00)")
        print("  3. Tối (18:00 - 21:00)")

        slot_choice = get_choice("Chọn ca (1/2/3)", ["1", "2", "3"])
        # Use shorter time slot codes to fit VARCHAR(5) limit
        time_slot = {
            "1": "Sáng",     # Morning (Sáng)
            "2": "Chiều",     # Afternoon (Chiều)
            "3": "Tối"     # Evening (Tối)
        }[slot_choice]

        result = self.service.create_session(
            lecturer_id=self.lecturer_id,
            subject_name=subject_name,
            time_slot=time_slot
        )

        if result["success"]:
            print_success(result["message"])
            data = result["data"]
            print(f"\n  ✅ THÔNG TIN BUỔI HỌC:")
            print(f"  - Mã buổi học: {data['session_id']}")
            print(f"  - Môn học: {data['subject_name']}")
            print(f"  - Ngày: {format_date(data['session_date'])}")
            print(f"  - Ca: {data['time_slot']}")
            print(f"  - 🔑 MÃ ĐIỂM DANH: {data['attendance_code']}")
            print_warning("Hãy chia sẻ mã điểm danh cho sinh viên!")
        else:
            print_error(result["message"])

        pause()

    def view_my_sessions(self):
        """Xem danh sách buổi học"""
        print_section("DANH SÁCH BUỔI HỌC CỦA TÔI")

        sessions = self.service.get_my_sessions(self.lecturer_id)

        if not sessions:
            print_info("Bạn chưa tạo buổi học nào.")
            pause()
            return

        headers = ["STT", "Mã buổi", "Môn học", "Ngày", "Ca", "Mã điểm danh"]
        rows = []

        # Map time slot codes to display names
        time_slot_display = {
            "AM": "Sáng",
            "PM": "Chiều",
            "EVE": "Tối"
        }

        for i, session in enumerate(sessions, 1):
            time_slot = session.get("time_slot", "")
            # Display friendly name if it's a code, otherwise show as-is
            time_slot_text = time_slot_display.get(time_slot, time_slot)

            rows.append([
                str(i),
                session.get("session_id", "")[:12] + "...",  # Rút gọn ID
                session.get("subject_name", ""),
                format_date(session.get("session_date", "")),
                time_slot_text,
                session.get("attendance_code", "")
            ])

        print_table(headers, rows)
        print(f"\n  Tổng số: {len(sessions)} buổi học")
        pause()

    def view_attendance(self):
        """Xem điểm danh theo buổi"""
        print_section("XEM ĐIỂM DANH THEO BUỔI HỌC")

        session_id = get_input("Nhập mã buổi học")

        attendances = self.service.view_attendance_by_session(session_id)

        if not attendances:
            print_info("Chưa có sinh viên nào điểm danh cho buổi học này.")
            pause()
            return

        headers = ["STT", "Mã SV", "Họ tên", "Lớp", "Trạng thái", "Thời gian điểm danh"]
        rows = []

        for i, att in enumerate(attendances, 1):
            status = att.get("status", "").lower()
            status_display = {
                "present": "✅ Có mặt",
                "absent": "❌ Vắng",
                "late": "⏰ Muộn"
            }.get(status, status)

            rows.append([
                str(i),
                att.get("student_id", ""),
                att.get("student_name", ""),
                att.get("class_name", ""),
                status_display,
                format_datetime(att.get("check_in_time", ""))
            ])

        print_table(headers, rows)
        print(f"\n  Tổng số sinh viên đã điểm danh: {len(attendances)}")
        pause()

    def update_attendance_status(self):
        """Cập nhật trạng thái điểm danh"""
        print_section("CẬP NHẬT TRẠNG THÁI ĐIỂM DANH")

        attendance_id = get_input("Nhập mã điểm danh (attendance_id)")

        print("\n  Chọn trạng thái mới:")
        print("  1. Có mặt (present)")
        print("  2. Vắng (absent)")
        print("  3. Đi muộn (late)")

        status_choice = get_choice("Chọn trạng thái (1/2/3)", ["1", "2", "3"])
        new_status = {
            "1": "present",
            "2": "absent",
            "3": "late"
        }[status_choice]

        if not confirm_action("Xác nhận cập nhật trạng thái?"):
            print_info("Đã hủy cập nhật.")
            pause()
            return

        result = self.service.update_attendance_status(attendance_id, new_status)

        if result["success"]:
            print_success(result["message"])
        else:
            print_error(result["message"])

        pause()

    def view_statistics(self):
        """Xem thống kê điểm danh"""
        print_section("THỐNG KÊ ĐIỂM DANH")

        session_id = get_input("Nhập mã buổi học")

        stats = self.service.get_session_statistics(session_id)

        print(f"\n  📊 THỐNG KÊ BUỔI HỌC: {session_id}")
        print(f"  - Tổng số sinh viên: {stats['total']}")
        print(f"  - ✅ Có mặt: {stats['present']}")
        print(f"  - ❌ Vắng: {stats['absent']}")
        print(f"  - ⏰ Đi muộn: {stats['late']}")

        if stats['total'] > 0:
            attendance_rate = (stats['present'] / stats['total']) * 100
            print(f"  - 📈 Tỷ lệ tham gia: {attendance_rate:.1f}%")

        pause()

    def create_announcement(self):
        """Tạo thông báo"""
        print_section("TẠO THÔNG BÁO")

        print("\n  Chọn đối tượng nhận thông báo:")
        print("  1. Tất cả (all)")
        print("  2. Sinh viên (student)")
        print("  3. Giảng viên (lecturer)")

        scope_choice = get_choice("Chọn đối tượng (1/2/3)", ["1", "2", "3"])
        scope = {
            "1": "all",
            "2": "student",
            "3": "lecturer"
        }[scope_choice]

        content = get_input("Nội dung thông báo")

        if not confirm_action("Xác nhận tạo thông báo?"):
            print_info("Đã hủy tạo thông báo.")
            pause()
            return

        result = self.service.create_announcement(
            lecturer_id=self.lecturer_id,
            content=content,
            scope=scope
        )

        if result["success"]:
            print_success(result["message"])
        else:
            print_error(result["message"])

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
