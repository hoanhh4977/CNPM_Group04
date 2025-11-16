"""
Utils Package
Các công cụ hỗ trợ cho ứng dụng
"""

from src.utils.id_generator import generate_student_id, generate_lecturer_id, generate_admin_id
from src.utils.validators import validate_phone, validate_username, validate_password
from src.utils.formatters import print_header, print_section, print_table, print_success, print_error, print_info

__all__ = [
    'generate_student_id',
    'generate_lecturer_id',
    'generate_admin_id',
    'validate_phone',
    'validate_username',
    'validate_password',
    'print_header',
    'print_section',
    'print_table',
    'print_success',
    'print_error',
    'print_info'
]
