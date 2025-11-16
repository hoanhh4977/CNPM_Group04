"""
ID Generator - Tạo các ID tự động cho hệ thống
"""
import uuid

def generate_student_id():
    """
    Tạo Student ID ngẫu nhiên
    Format: S + UUID (8 ký tự đầu)
    Ví dụ: S_a3b4c5d6
    """
    return f"S_{str(uuid.uuid4())[:8]}"

def generate_lecturer_id():
    """
    Tạo Lecturer ID ngẫu nhiên
    Format: L + UUID (8 ký tự đầu)
    Ví dụ: L_x9y8z7w6
    """
    return f"L_{str(uuid.uuid4())[:8]}"

def generate_admin_id():
    """
    Tạo Admin ID ngẫu nhiên
    Format: A + UUID (8 ký tự đầu)
    Ví dụ: A_m1n2o3p4
    """
    return f"A_{str(uuid.uuid4())[:8]}"

def generate_user_id():
    """
    Tạo User ID ngẫu nhiên
    Format: UUID đầy đủ
    Ví dụ: 550e8400-e29b-41d4-a716-446655440000
    """
    return str(uuid.uuid4())

def generate_attendance_id():
    """
    Tạo Attendance ID ngẫu nhiên
    Format: ATT + UUID (8 ký tự đầu)
    Ví dụ: ATT_a1b2c3d4
    """
    return f"ATT_{str(uuid.uuid4())[:8]}"

def generate_session_id():
    """
    Tạo Session ID ngẫu nhiên
    Format: SES + UUID (8 ký tự đầu)
    Ví dụ: SES_q1w2e3r4
    """
    return f"SES_{str(uuid.uuid4())[:8]}"

def generate_notification_id():
    """
    Tạo Notification ID ngẫu nhiên
    Format: NOT + UUID (8 ký tự đầu)
    Ví dụ: NOT_z9y8x7w6
    """
    return f"NOT_{str(uuid.uuid4())[:8]}"
