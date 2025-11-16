"""
Pytest configuration and fixtures
"""
import pytest
from unittest.mock import Mock, MagicMock


@pytest.fixture
def mock_supabase_client():
    """Mock Supabase client for testing"""
    mock_client = MagicMock()
    mock_table = MagicMock()

    # Setup default mock behavior
    mock_client.table.return_value = mock_table
    mock_table.select.return_value = mock_table
    mock_table.insert.return_value = mock_table
    mock_table.update.return_value = mock_table
    mock_table.delete.return_value = mock_table
    mock_table.eq.return_value = mock_table
    mock_table.execute.return_value = MagicMock(data=[])

    return mock_client


@pytest.fixture
def sample_user():
    """Sample user data for testing"""
    return {
        "user_id": "test_user_123",
        "username": "testuser",
        "full_name": "Test User",
        "account_type": "student",
        "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILSBiui4G",  # "password123"
        "phone_number": "0901234567",
        "address": "Test Address"
    }


@pytest.fixture
def sample_student(sample_user):
    """Sample student data for testing"""
    return {
        "student_id": "S_test123",
        "user_id": sample_user["user_id"],
        "class_name": "K23CNTT",
        **sample_user
    }


@pytest.fixture
def sample_lecturer(sample_user):
    """Sample lecturer data for testing"""
    user = sample_user.copy()
    user["account_type"] = "lecturer"
    return {
        "lecturer_id": "L_test123",
        "user_id": user["user_id"],
        **user
    }


@pytest.fixture
def sample_admin(sample_user):
    """Sample admin data for testing"""
    user = sample_user.copy()
    user["account_type"] = "admin"
    return {
        "admin_id": "A_test123",
        "user_id": user["user_id"],
        "admin_level": 3,
        **user
    }


@pytest.fixture
def sample_session():
    """Sample session data for testing"""
    return {
        "session_id": "SES_test123",
        "lecturer_id": "L_test123",
        "session_date": "2024-01-15",
        "time_slot": "Sáng",
        "subject_name": "Lập trình Python",
        "attendance_code": "ABC123"
    }


@pytest.fixture
def sample_attendance():
    """Sample attendance data for testing"""
    return {
        "attendance_id": "ATT_test123",
        "student_id": "S_test123",
        "session_id": "SES_test123",
        "status": "present",
        "check_in_time": "2024-01-15T08:30:00"
    }
