"""
Main Menu - Menu chính của hệ thống
Xử lý đăng nhập / đăng ký
"""

from src.services.auth_service import AuthService
from src.utils.formatters import print_header, print_menu, print_success, print_error
from src.ui.helpers import get_input, get_password, get_phone, get_choice, pause


class MainMenu:
    def __init__(self):
        """Khởi tạo Main Menu"""
        self.auth_service = AuthService()
        self.current_user = None

    def run(self):
        """
        Chạy menu chính

        Trả về:
            dict hoặc None: Thông tin user nếu đăng nhập thành công, None nếu thoát
        """
        while True:
            print_header("HỆ THỐNG QUẢN LÝ ĐIỂM DANH SINH VIÊN")
            print_menu("MENU CHÍNH", [
                ("1", "Đăng nhập"),
                ("2", "Đăng ký"),
                ("0", "Thoát chương trình")
            ], show_back=False)

            choice = get_input("Lựa chọn của bạn")

            if choice == "1":
                user = self.handle_login()
                if user:
                    return user
            elif choice == "2":
                self.handle_register()
            elif choice == "0":
                print_success("Cảm ơn bạn đã sử dụng hệ thống. Tạm biệt!")
                return None
            else:
                print_error("Lựa chọn không hợp lệ!")
                pause()

    def handle_login(self):
        """
        Xử lý đăng nhập

        Trả về:
            dict hoặc None: Thông tin user nếu thành công, None nếu thất bại
        """
        print_header("ĐĂNG NHẬP")

        username = get_input("Tên đăng nhập hoặc số điện thoại")
        password = get_password()

        result = self.auth_service.login({
            "username": username,
            "password": password
        })

        if result["success"]:
            user = result["data"]
            print_success(f"Đăng nhập thành công! Xin chào {user['full_name']}")
            pause()
            return user
        else:
            print_error(result["error"])
            pause()
            return None

    def handle_register(self):
        """Xử lý đăng ký"""
        print_header("ĐĂNG KÝ TÀI KHOẢN MỚI")

        # Thông tin cơ bản
        print("\n  📝 THÔNG TIN CƠ BẢN")
        username = get_input("Tên đăng nhập (ít nhất 3 ký tự)")
        full_name = get_input("Họ và tên đầy đủ")
        password = get_password("Mật khẩu (ít nhất 6 ký tự)")
        phone_number = get_phone()
        address = get_input("Địa chỉ")

        # Chọn loại tài khoản
        print("\n  👤 LOẠI TÀI KHOẢN")
        print("  1. Sinh viên")
        print("  2. Giảng viên")

        role_choice = get_choice("Nhập lựa chọn (1/2)", ["1", "2"])
        account_type = "student" if role_choice == "1" else "lecturer"

        # Thông tin bổ sung
        extra = {}
        if account_type == "student":
            print("\n  🎓 THÔNG TIN SINH VIÊN")
            from src.utils.id_generator import generate_student_id
            extra["student_id"] = generate_student_id()
            extra["class_name"] = get_input("Lớp học (vd: K23CNTT)")
            print(f"  ℹ️  Mã sinh viên của bạn: {extra['student_id']}")
        else:
            print("\n  👨‍🏫 THÔNG TIN GIẢNG VIÊN")
            from src.utils.id_generator import generate_lecturer_id
            extra["lecturer_id"] = generate_lecturer_id()
            print(f"  ℹ️  Mã giảng viên của bạn: {extra['lecturer_id']}")

        # Xác nhận thông tin
        print("\n  ✅ XÁC NHẬN THÔNG TIN")
        print(f"  - Tên đăng nhập: {username}")
        print(f"  - Họ tên: {full_name}")
        print(f"  - Vai trò: {'Sinh viên' if account_type == 'student' else 'Giảng viên'}")
        print(f"  - Số điện thoại: {phone_number}")
        print(f"  - Địa chỉ: {address}")
        if account_type == "student":
            print(f"  - Lớp học: {extra['class_name']}")

        if not get_choice("Xác nhận đăng ký? (y/n)", ["y", "n", "Y", "N"]).lower() == 'y':
            print_error("Đã hủy đăng ký!")
            pause()
            return

        # Thực hiện đăng ký
        user_data = {
            "username": username,
            "full_name": full_name,
            "password": password,
            "phone_number": phone_number,
            "address": address,
            "account_type": account_type,
            "extra": extra
        }

        result = self.auth_service.register(user_data)

        if result["success"]:
            print_success(result["message"])
            print("  ℹ️  Vui lòng đăng nhập để sử dụng hệ thống")
        else:
            print_error(result["error"])

        pause()
