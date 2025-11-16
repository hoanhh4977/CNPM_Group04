"""
Admin Menu - Menu dành cho Quản trị viên
"""

from src.services.admin_service import AdminService
from src.utils.formatters import (
    print_header, print_menu, print_section, print_table,
    print_success, print_error, print_info, format_datetime
)
from src.ui.helpers import get_input, get_choice, get_phone, pause, confirm_action


class AdminMenu:
    def __init__(self, user_data: dict):
        """
        Khởi tạo Admin Menu

        Tham số:
            user_data: Dict chứa thông tin user đã đăng nhập
        """
        self.user_data = user_data
        self.admin_id = user_data.get("admin_id")
        self.admin_level = user_data.get("admin_level", 1)
        self.full_name = user_data.get("full_name")
        self.service = AdminService()

    def run(self):
        """Chạy menu admin"""
        while True:
            print_header(f"MENU QUẢN TRỊ - {self.full_name}")
            print(f"  Admin ID: {self.admin_id} | Level: {self.admin_level}\n")

            print_menu("CHỨC NĂNG", [
                ("1", "Quản lý người dùng"),
                ("2", "Quản lý thông báo"),
                ("3", "Thống kê hệ thống"),
                ("0", "Đăng xuất")
            ], show_back=False)

            choice = get_input("Lựa chọn của bạn")

            if choice == "1":
                self.user_management_menu()
            elif choice == "2":
                self.announcement_management_menu()
            elif choice == "3":
                self.view_statistics()
            elif choice == "0":
                print_success("Đăng xuất thành công!")
                break
            else:
                print_error("Lựa chọn không hợp lệ!")
                pause()

    # ==================== HELPER METHODS ====================

    def _find_user_by_identifier(self, identifier: str):
        """
        Tìm user bằng User ID, username hoặc phone number

        Tham số:
            identifier: User ID, Username hoặc số điện thoại

        Trả về:
            dict hoặc None: Thông tin user nếu tìm thấy
        """
        from src.storage.repositories import UserRepository
        user_repo = UserRepository()

        # Thử tìm bằng User ID
        user = user_repo.get_user_by_id(identifier)
        if user:
            return user

        # Thử tìm bằng username
        user = user_repo.get_user_by_username(identifier)
        if user:
            return user

        # Thử tìm bằng phone
        user = user_repo.get_user_by_phone(identifier)
        return user

    # ==================== QUẢN LÝ NGƯỜI DÙNG ====================

    def user_management_menu(self):
        """Menu quản lý người dùng"""
        while True:
            print_section("QUẢN LÝ NGƯỜI DÙNG")

            print_menu("", [
                ("1", "Xem danh sách người dùng"),
                ("2", "Cập nhật thông tin người dùng"),
                ("3", "Đổi vai trò người dùng"),
                ("4", "Xóa người dùng"),
                ("0", "Quay lại")
            ], show_back=False)

            choice = get_input("Lựa chọn của bạn")

            if choice == "1":
                self.view_users()
            elif choice == "2":
                self.update_user_info()
            elif choice == "3":
                self.change_user_role()
            elif choice == "4":
                self.delete_user()
            elif choice == "0":
                break
            else:
                print_error("Lựa chọn không hợp lệ!")
                pause()

    def view_users(self):
        """Xem danh sách người dùng"""
        print_section("DANH SÁCH NGƯỜI DÙNG")

        users = self.service.get_all_users()

        if not users:
            print_info("Không có người dùng nào.")
            pause()
            return

        # Lọc bỏ các user có dữ liệu không hợp lệ (None)
        valid_users = [u for u in users if u.get("full_name") is not None]

        if not valid_users:
            print_info("Không có người dùng hợp lệ nào.")
            pause()
            return

        headers = ["STT", "User ID", "Username", "Họ tên", "Loại TK", "SĐT"]
        rows = []

        for i, user in enumerate(valid_users, 1):
            account_type_display = {
                "student": "🎓 Sinh viên",
                "lecturer": "👨‍🏫 Giảng viên",
                "admin": "👑 Admin"
            }.get(user.get("account_type"), user.get("account_type", ""))

            rows.append([
                str(i),
                user.get("user_id", ""),
                user.get("username", ""),
                user.get("full_name", ""),
                account_type_display,
                user.get("phone_number", "")
            ])

        print_table(headers, rows)
        print(f"\n  Tổng số: {len(valid_users)} người dùng")
        print_info("💡 Mẹo: Bạn có thể sử dụng User ID, Username hoặc SĐT để thực hiện các thao tác")
        pause()

    def update_user_info(self):
        """Cập nhật thông tin người dùng"""
        print_section("CẬP NHẬT THÔNG TIN NGƯỜI DÙNG")

        identifier = get_input("Nhập User ID / Username / SĐT của user cần cập nhật")

        # Tìm user bằng username hoặc phone
        user = self._find_user_by_identifier(identifier)
        if not user:
            print_error("Không tìm thấy người dùng!")
            pause()
            return

        print_info(f"Tìm thấy: {user.get('full_name')} (@{user.get('username')})")

        print("\n  Nhập thông tin mới (để trống nếu không muốn thay đổi):")
        phone = input("  Số điện thoại mới: ").strip()
        address = input("  Địa chỉ mới: ").strip()

        if not phone and not address:
            print_info("Không có thông tin nào được cập nhật.")
            pause()
            return

        if not confirm_action("Xác nhận cập nhật?"):
            print_info("Đã hủy cập nhật.")
            pause()
            return

        result = self.service.update_user_info(
            user_id_to_update=user.get("user_id"),
            updater_admin_level=self.admin_level,
            phone=phone if phone else None,
            address=address if address else None
        )

        if result["success"]:
            print_success(result["message"])
        else:
            print_error(result["message"])

        pause()

    def change_user_role(self):
        """Đổi vai trò người dùng"""
        print_section("ĐỔI VAI TRÒ NGƯỜI DÙNG")

        identifier = get_input("Nhập User ID / Username / SĐT của user cần đổi vai trò")

        # Tìm user bằng username hoặc phone
        user = self._find_user_by_identifier(identifier)
        if not user:
            print_error("Không tìm thấy người dùng!")
            pause()
            return

        print_info(f"Tìm thấy: {user.get('full_name')} (@{user.get('username')}) - Vai trò hiện tại: {user.get('account_type')}")

        print("\n  Chọn vai trò mới:")
        print("  1. Sinh viên (student)")
        print("  2. Giảng viên (lecturer)")

        role_choice = get_choice("Chọn vai trò (1/2)", ["1", "2"])
        new_account_type = "student" if role_choice == "1" else "lecturer"

        # Tạo role ID mới
        if new_account_type == "student":
            from src.utils.id_generator import generate_student_id
            new_role_id = generate_student_id()
            print(f"\n  ℹ️  Student ID mới: {new_role_id}")
        else:
            from src.utils.id_generator import generate_lecturer_id
            new_role_id = generate_lecturer_id()
            print(f"\n  ℹ️  Lecturer ID mới: {new_role_id}")

        if not confirm_action("Xác nhận đổi vai trò?"):
            print_info("Đã hủy đổi vai trò.")
            pause()
            return

        result = self.service.update_user_info(
            user_id_to_update=user.get("user_id"),
            updater_admin_level=self.admin_level,
            new_account_type=new_account_type,
            new_role_id=new_role_id
        )

        if result["success"]:
            print_success(result["message"])
        else:
            print_error(result["message"])

        pause()

    def delete_user(self):
        """Xóa người dùng"""
        print_section("XÓA NGƯỜI DÙNG")

        identifier = get_input("Nhập User ID / Username / SĐT của user cần xóa")

        # Tìm user bằng username hoặc phone
        user = self._find_user_by_identifier(identifier)
        if not user:
            print_error("Không tìm thấy người dùng!")
            pause()
            return

        print_info(f"Tìm thấy: {user.get('full_name')} (@{user.get('username')})")

        if not confirm_action("⚠️  BẠN CHẮC CHẮN MUỐN XÓA NGƯỜI DÙNG NÀY?"):
            print_info("Đã hủy xóa.")
            pause()
            return

        result = self.service.delete_user(
            user_id_to_delete=user.get("user_id"),
            deleter_admin_level=self.admin_level
        )

        if result["success"]:
            print_success(result["message"])
        else:
            print_error(result["message"])

        pause()

    # ==================== QUẢN LÝ THÔNG BÁO ====================

    def announcement_management_menu(self):
        """Menu quản lý thông báo"""
        while True:
            print_section("QUẢN LÝ THÔNG BÁO")

            print_menu("", [
                ("1", "Tạo thông báo mới"),
                ("2", "Xem tất cả thông báo"),
                ("3", "Cập nhật thông báo"),
                ("4", "Xóa thông báo"),
                ("0", "Quay lại")
            ], show_back=False)

            choice = get_input("Lựa chọn của bạn")

            if choice == "1":
                self.create_announcement()
            elif choice == "2":
                self.view_announcements()
            elif choice == "3":
                self.update_announcement()
            elif choice == "4":
                self.delete_announcement()
            elif choice == "0":
                break
            else:
                print_error("Lựa chọn không hợp lệ!")
                pause()

    def create_announcement(self):
        """Tạo thông báo"""
        print_section("TẠO THÔNG BÁO MỚI")

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
            admin_id=self.admin_id,
            content=content,
            scope=scope
        )

        if result["success"]:
            print_success(result["message"])
        else:
            print_error(result["message"])

        pause()

    def view_announcements(self):
        """Xem tất cả thông báo"""
        print_section("TẤT CẢ THÔNG BÁO")

        announcements = self.service.get_all_announcements()

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
            print(f"     ID: {announcement.get('notification_id', '')}")
            print(f"     📅 {format_datetime(announcement.get('creation_date', ''))}")
            print(f"     📝 {announcement.get('content', '')}")
            print("     " + "-" * 50)

        print(f"\n  Tổng số: {len(announcements)} thông báo")
        pause()

    def update_announcement(self):
        """Cập nhật thông báo"""
        print_section("CẬP NHẬT THÔNG BÁO")

        print_info("Gợi ý: Chạy 'Xem tất cả thông báo' để lấy ID")
        notification_id = get_input("Nhập Notification ID")
        new_content = get_input("Nội dung mới")

        if not confirm_action("Xác nhận cập nhật?"):
            print_info("Đã hủy cập nhật.")
            pause()
            return

        result = self.service.update_announcement(notification_id, new_content)

        if result["success"]:
            print_success(result["message"])
        else:
            print_error(result["message"])

        pause()

    def delete_announcement(self):
        """Xóa thông báo"""
        print_section("XÓA THÔNG BÁO")

        print_info("Gợi ý: Chạy 'Xem tất cả thông báo' để lấy ID")
        notification_id = get_input("Nhập Notification ID")

        if not confirm_action("⚠️  Xác nhận xóa thông báo?"):
            print_info("Đã hủy xóa.")
            pause()
            return

        result = self.service.delete_announcement(notification_id)

        if result["success"]:
            print_success(result["message"])
        else:
            print_error(result["message"])

        pause()

    # ==================== THỐNG KÊ ====================

    def view_statistics(self):
        """Xem thống kê hệ thống"""
        print_section("THỐNG KÊ HỆ THỐNG")

        stats = self.service.get_system_statistics()

        print("\n  📊 THỐNG KÊ TỔNG QUAN:")
        print(f"  - 👥 Tổng số người dùng: {stats['total_users']}")
        print(f"  - 🎓 Sinh viên: {stats['total_students']}")
        print(f"  - 👨‍🏫 Giảng viên: {stats['total_lecturers']}")
        print(f"  - 👑 Quản trị viên: {stats['total_admins']}")
        print(f"  - 📚 Tổng số buổi học: {stats['total_sessions']}")
        print(f"  - ✅ Tổng số điểm danh: {stats['total_attendances']}")
        print(f"  - 📢 Tổng số thông báo: {stats['total_announcements']}")

        pause()
