"""
Validators - Kiểm tra tính hợp lệ của dữ liệu đầu vào
"""

def validate_phone(phone_number: str) -> bool:
    """
    Kiểm tra số điện thoại hợp lệ
    Quy tắc: Phải là 10 chữ số
    """
    if not phone_number:
        return False
    return phone_number.isdigit() and len(phone_number) == 10

def validate_username(username: str) -> bool:
    """
    Kiểm tra username hợp lệ
    Quy tắc: Ít nhất 3 ký tự, không chứa khoảng trắng
    """
    if not username or len(username) < 3:
        return False
    if ' ' in username:
        return False
    return True

def validate_password(password: str) -> bool:
    """
    Kiểm tra mật khẩu hợp lệ
    Quy tắc: Ít nhất 6 ký tự
    """
    if not password or len(password) < 6:
        return False
    return True

def validate_account_type(account_type: str) -> bool:
    """
    Kiểm tra loại tài khoản hợp lệ
    Quy tắc: Phải là student, lecturer, hoặc admin
    """
    valid_types = ['student', 'lecturer', 'admin']
    return account_type in valid_types

def validate_attendance_status(status: str) -> bool:
    """
    Kiểm tra trạng thái điểm danh hợp lệ
    Quy tắc: Phải là present, absent, hoặc late
    """
    valid_statuses = ['present', 'absent', 'late']
    return status.lower() in valid_statuses

def validate_not_empty(value: str, field_name: str = "Trường") -> tuple:
    """
    Kiểm tra giá trị không được để trống
    Returns: (is_valid: bool, message: str)
    """
    if not value or not value.strip():
        return (False, f"{field_name} không được để trống!")
    return (True, "")

def validate_choice(choice: str, valid_choices: list) -> bool:
    """
    Kiểm tra lựa chọn có trong danh sách hợp lệ
    """
    return choice in valid_choices
