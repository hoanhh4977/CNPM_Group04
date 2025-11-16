"""
Unit tests for utilities
"""
import pytest
from src.utils.id_generator import (
    generate_student_id, generate_lecturer_id, generate_admin_id,
    generate_user_id, generate_attendance_id, generate_session_id
)
from src.utils.validators import (
    validate_phone, validate_username, validate_password,
    validate_account_type, validate_attendance_status
)
from utils import generate_attendance_code


class TestIDGenerator:
    """Test ID generation functions"""

    def test_generate_student_id(self):
        """Test student ID generation"""
        student_id = generate_student_id()
        assert student_id.startswith("S_")
        assert len(student_id) == 10  # S_ + 8 chars

    def test_generate_lecturer_id(self):
        """Test lecturer ID generation"""
        lecturer_id = generate_lecturer_id()
        assert lecturer_id.startswith("L_")
        assert len(lecturer_id) == 10

    def test_generate_admin_id(self):
        """Test admin ID generation"""
        admin_id = generate_admin_id()
        assert admin_id.startswith("A_")
        assert len(admin_id) == 10

    def test_generate_user_id(self):
        """Test user ID generation (UUID)"""
        user_id = generate_user_id()
        assert len(user_id) == 36  # UUID format
        assert user_id.count('-') == 4

    def test_generate_attendance_id(self):
        """Test attendance ID generation"""
        att_id = generate_attendance_id()
        assert att_id.startswith("ATT_")

    def test_generate_session_id(self):
        """Test session ID generation"""
        session_id = generate_session_id()
        assert session_id.startswith("SES_")

    def test_generate_attendance_code(self):
        """Test attendance code generation"""
        code = generate_attendance_code()
        assert len(code) == 6
        assert code.isalnum()
        assert code.isupper() or code.isdigit()


class TestValidators:
    """Test validation functions"""

    def test_validate_phone_valid(self):
        """Test valid phone numbers"""
        assert validate_phone("0901234567") is True
        assert validate_phone("0123456789") is True

    def test_validate_phone_invalid(self):
        """Test invalid phone numbers"""
        assert validate_phone("123") is False
        assert validate_phone("abcdefghij") is False
        assert validate_phone("") is False
        assert validate_phone("090123456") is False  # 9 digits

    def test_validate_username_valid(self):
        """Test valid usernames"""
        assert validate_username("user123") is True
        assert validate_username("test_user") is True

    def test_validate_username_invalid(self):
        """Test invalid usernames"""
        assert validate_username("ab") is False  # Too short
        assert validate_username("user name") is False  # Has space
        assert validate_username("") is False

    def test_validate_password_valid(self):
        """Test valid passwords"""
        assert validate_password("password123") is True
        assert validate_password("123456") is True

    def test_validate_password_invalid(self):
        """Test invalid passwords"""
        assert validate_password("12345") is False  # Too short
        assert validate_password("") is False

    def test_validate_account_type(self):
        """Test account type validation"""
        assert validate_account_type("student") is True
        assert validate_account_type("lecturer") is True
        assert validate_account_type("admin") is True
        assert validate_account_type("invalid") is False

    def test_validate_attendance_status(self):
        """Test attendance status validation"""
        assert validate_attendance_status("present") is True
        assert validate_attendance_status("absent") is True
        assert validate_attendance_status("late") is True
        assert validate_attendance_status("PRESENT") is True  # Case insensitive
        assert validate_attendance_status("invalid") is False
