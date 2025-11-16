import random
import string

def generate_attendance_code(length=5):
    """
    Tạo mã điểm danh ngẫu nhiên
    Mặc định: 6 ký tự (chữ in hoa + số)
    Ví dụ: "A3K9B2"
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
