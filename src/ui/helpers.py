"""
UI Helpers - Các hàm hỗ trợ giao diện
"""

import getpass
from src.utils.validators import validate_phone, validate_username, validate_password


def get_input(prompt: str, required: bool = True) -> str:
    """
    Lấy input từ người dùng

    Tham số:
        prompt: Câu nhắc
        required: Bắt buộc nhập hay không

    Trả về:
        str: Giá trị người dùng nhập
    """
    while True:
        value = input(f"  {prompt}: ").strip()
        if not required or value:
            return value
        print("  ❌ Không được để trống!")


def get_password(prompt: str = "Mật khẩu") -> str:
    """
    Lấy mật khẩu từ người dùng (ẩn ký tự)

    Trả về:
        str: Mật khẩu
    """
    while True:
        password = getpass.getpass(f"  {prompt}: ")
        if password:
            return password
        print("  ❌ Mật khẩu không được để trống!")


def get_phone() -> str:
    """
    Lấy số điện thoại hợp lệ từ người dùng

    Trả về:
        str: Số điện thoại (10 chữ số)
    """
    while True:
        phone = get_input("Số điện thoại (10 chữ số)")
        if validate_phone(phone):
            return phone
        print("  ❌ Số điện thoại không hợp lệ! Phải là 10 chữ số.")


def get_choice(prompt: str, valid_choices: list) -> str:
    """
    Lấy lựa chọn hợp lệ từ người dùng

    Tham số:
        prompt: Câu nhắc
        valid_choices: List các lựa chọn hợp lệ

    Trả về:
        str: Lựa chọn
    """
    while True:
        choice = get_input(prompt).strip()
        if choice in valid_choices:
            return choice
        print(f"  ❌ Lựa chọn không hợp lệ! Vui lòng chọn: {', '.join(valid_choices)}")


def confirm_action(message: str) -> bool:
    """
    Xác nhận hành động từ người dùng

    Tham số:
        message: Câu hỏi xác nhận

    Trả về:
        bool: True nếu xác nhận, False nếu hủy
    """
    choice = get_choice(f"{message} (y/n)", ['y', 'n', 'Y', 'N'])
    return choice.lower() == 'y'


def pause():
    """Tạm dừng chờ người dùng nhấn Enter"""
    input("\n  Nhấn Enter để tiếp tục...")


def clear_screen():
    """Xóa màn hình console"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
