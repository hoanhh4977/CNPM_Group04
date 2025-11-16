"""
HỆ THỐNG QUẢN LÝ ĐIỂM DANH SINH VIÊN
Student Attendance Management System

Entry point chính của ứng dụng
"""

from src.ui.main_menu import MainMenu
from src.ui.student_menu import StudentMenu
from src.ui.lecturer_menu import LecturerMenu
from src.ui.admin_menu import AdminMenu
from src.utils.formatters import print_header, print_error


def main():
    """
    Hàm chính của chương trình

    Luồng hoạt động:
    1. Hiển thị màn hình đăng nhập/đăng ký
    2. Sau khi đăng nhập thành công, chuyển đến menu tương ứng:
       - student -> StudentMenu
       - lecturer -> LecturerMenu
       - admin -> AdminMenu
    3. Khi đăng xuất, quay lại bước 1
    """
    print_header("CHÀO MỪNG ĐẾN VỚI HỆ THỐNG QUẢN LÝ ĐIỂM DANH")
    print("  🎓 Dành cho Sinh viên, Giảng viên và Quản trị viên")
    print("\n  Nhấn Enter để bắt đầu...")
    input()

    while True:
        # Bước 1: Đăng nhập / Đăng ký
        main_menu = MainMenu()
        user_data = main_menu.run()

        # Nếu người dùng chọn thoát (user_data = None)
        if not user_data:
            break

        # Bước 2: Chuyển đến menu tương ứng dựa trên account_type
        account_type = user_data.get("account_type")

        try:
            if account_type == "student":
                menu = StudentMenu(user_data)
                menu.run()

            elif account_type == "lecturer":
                menu = LecturerMenu(user_data)
                menu.run()

            elif account_type == "admin":
                menu = AdminMenu(user_data)
                menu.run()

            else:
                print_error(f"Loại tài khoản không hợp lệ: {account_type}")
                break

        except KeyboardInterrupt:
            print("\n\n  ⚠️  Phát hiện Ctrl+C - Đăng xuất...")
            continue

        except Exception as e:
            print_error(f"Lỗi không mong đợi: {str(e)}")
            print("  Vui lòng thử lại hoặc liên hệ quản trị viên.")
            input("\n  Nhấn Enter để tiếp tục...")
            continue


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  👋 Tạm biệt! Hẹn gặp lại.")
    except Exception as e:
        print_error(f"Lỗi nghiêm trọng: {str(e)}")
        print("  Chương trình sẽ đóng. Vui lòng báo cáo lỗi này cho quản trị viên.")
