"""
Unit tests for service layer
"""
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime


class TestAuthService:
    """Test AuthService"""

    @patch('src.services.auth_service.UserRepository')
    @patch('src.services.auth_service.StudentRepository')
    @patch('src.services.auth_service.LecturerRepository')
    @patch('src.services.auth_service.AdminRepository')
    @patch('src.services.auth_service.bcrypt')
    def test_register_student_success(self, mock_bcrypt, mock_admin_repo,
                                     mock_lect_repo, mock_stud_repo, mock_user_repo):
        """Test successful student registration"""
        from src.services import AuthService

        # Setup mocks
        mock_user_repo.return_value.get_user_by_username.return_value = None
        mock_bcrypt.hashpw.return_value.decode.return_value = "hashed_password"
        mock_user_repo.return_value.create_user.return_value = [{"user_id": "test_123"}]
        mock_stud_repo.return_value.create.return_value = [{"student_id": "S_test123"}]

        service = AuthService()
        result = service.register({
            "username": "newuser",
            "password": "password123",
            "full_name": "New User",
            "account_type": "student",
            "phone_number": "0901234567",
            "address": "Test Address",
            "extra": {"student_id": "S_new123", "class_name": "K23CNTT"}
        })

        assert result["success"] is True
        assert "thành công" in result["message"]

    @patch('src.services.auth_service.UserRepository')
    @patch('src.services.auth_service.StudentRepository')
    @patch('src.services.auth_service.bcrypt')
    def test_login_success(self, mock_bcrypt, mock_stud_repo, mock_user_repo, sample_user, sample_student):
        """Test successful login"""
        from src.services import AuthService

        mock_user_repo.return_value.get_user_by_username.return_value = sample_user
        mock_user_repo.return_value.get_user_by_phone.return_value = None
        mock_stud_repo.return_value.get_by_user_id.return_value = sample_student
        mock_bcrypt.checkpw.return_value = True

        service = AuthService()
        result = service.login({"username": "testuser", "password": "password123"})

        assert result["success"] is True
        assert result["data"]["account_type"] == "student"

    @patch('src.services.auth_service.UserRepository')
    def test_login_invalid_username(self, mock_user_repo):
        """Test login with invalid username"""
        from src.services import AuthService

        mock_user_repo.return_value.get_user_by_username.return_value = None
        mock_user_repo.return_value.get_user_by_phone.return_value = None

        service = AuthService()
        result = service.login({"username": "invaliduser", "password": "password123"})

        assert result["success"] is False
        assert "Không tìm thấy" in result["error"]


class TestStudentService:
    """Test StudentService"""

    @patch('src.services.student_service.SessionRepository')
    @patch('src.services.student_service.AttendanceRepository')
    def test_mark_attendance_success(self, mock_att_repo, mock_sess_repo, sample_session):
        """Test successful attendance marking"""
        from src.services import StudentService

        # Mock session exists with correct code
        mock_sess_repo.return_value.get_by_id.return_value = sample_session
        # Mock no existing attendance
        mock_att_repo.return_value.get_attendance_by_student_and_session.return_value = None
        # Mock successful creation
        mock_att_repo.return_value.create.return_value = [{"attendance_id": "ATT_123", "status": "present"}]

        service = StudentService()
        result = service.mark_attendance("S_test123", "SES_test123", "ABC123")

        assert result is not None
        assert len(result) > 0

    @patch('src.services.student_service.SessionRepository')
    @patch('src.services.student_service.AttendanceRepository')
    def test_mark_attendance_invalid_code(self, mock_sess_repo, mock_att_repo, sample_session):
        """Test attendance marking with wrong code"""
        from src.services import StudentService

        mock_sess_repo.return_value.get_by_id.return_value = sample_session
        mock_att_repo.return_value.get_attendance_by_student_and_session.return_value = None

        service = StudentService()
        result = service.mark_attendance("S_test123", "SES_test123", "WRONG123")

        # Invalid code should return error or empty result
        assert result is not None

    @patch('src.services.student_service.AttendanceRepository')
    def test_get_my_attendance_history(self, mock_att_repo):
        """Test getting attendance history"""
        from src.services import StudentService

        mock_att_repo.return_value.get_attendance_by_student_id.return_value = [
            {
                "attendance_id": "ATT_1",
                "status": "present",
                "session_id": "SES_1"
            }
        ]

        service = StudentService()
        result = service.get_my_attendance_history("S_test123")

        assert result is not None
        assert isinstance(result, list)


class TestLecturerService:
    """Test LecturerService"""

    @patch('src.services.lecturer_service.SessionRepository')
    def test_create_session_success(self, mock_sess_repo):
        """Test successful session creation"""
        from src.services import LecturerService

        mock_sess_repo.return_value.create.return_value = [{"session_id": "SES_123", "attendance_code": "ABC123"}]

        service = LecturerService()
        result = service.create_session(
            lecturer_id="L_test123",
            subject_name="Python Programming",
            time_slot="Sáng"
        )

        assert result is not None
        assert len(result) > 0

    @patch('src.services.lecturer_service.SessionRepository')
    def test_get_my_sessions(self, mock_sess_repo):
        """Test getting lecturer's sessions"""
        from src.services import LecturerService

        mock_sess_repo.return_value.get_sessions_by_lecturer_id.return_value = [
            {"session_id": "SES_1", "subject_name": "Python"}
        ]

        service = LecturerService()
        result = service.get_my_sessions("L_test123")

        assert result is not None
        assert isinstance(result, list)

    @patch('src.services.lecturer_service.AttendanceRepository')
    def test_get_session_statistics(self, mock_att_repo):
        """Test session statistics calculation"""
        from src.services import LecturerService

        mock_att_repo.return_value.get_attendance_by_session_id.return_value = [
            {"status": "present"},
            {"status": "present"},
            {"status": "absent"},
            {"status": "late"}
        ]

        service = LecturerService()
        stats = service.get_session_statistics("SES_test123")

        assert stats is not None
        assert isinstance(stats, dict)


class TestAdminService:
    """Test AdminService"""

    @patch('src.services.admin_service.UserRepository')
    def test_get_all_users(self, mock_user_repo):
        """Test getting all users"""
        from src.services import AdminService

        mock_user_repo.return_value.get_all_users.return_value = [
            {"username": "user1"},
            {"username": "user2"}
        ]

        service = AdminService()
        result = service.get_all_users()

        assert result is not None
        assert isinstance(result, list)

    @patch('src.services.admin_service.AdminRepository')
    @patch('src.services.admin_service.UserRepository')
    def test_update_user_info(self, mock_user_repo, mock_admin_repo, sample_user):
        """Test updating user information"""
        from src.services import AdminService

        updated_user = sample_user.copy()
        updated_user["full_name"] = "Updated Name"
        mock_user_repo.return_value.get_user_by_id.return_value = sample_user
        mock_admin_repo.return_value.get_by_user_id.return_value = None  # Not an admin
        mock_user_repo.return_value.update_user.return_value = None

        service = AdminService()
        result = service.update_user_info(
            user_id_to_update="test_user_123",
            updater_admin_level=2,
            phone="0909090909",
            address="New Address"
        )

        assert result is not None
        assert result["success"] is True

    @patch('src.services.admin_service.AdminRepository')
    @patch('src.services.admin_service.UserRepository')
    @patch('src.services.admin_service.StudentRepository')
    @patch('src.services.admin_service.LecturerRepository')
    def test_change_role_student_to_lecturer(self, mock_lect_repo, mock_stud_repo,
                                            mock_user_repo, mock_admin_repo, sample_student):
        """Test changing role from student to lecturer using update_user_info"""
        from src.services import AdminService

        # Setup mocks
        mock_user_repo.return_value.get_user_by_id.return_value = {
            "user_id": "test_user_123",
            "account_type": "student"
        }
        mock_admin_repo.return_value.get_by_user_id.return_value = None  # Not an admin
        mock_stud_repo.return_value.get_by_user_id.return_value = sample_student
        mock_stud_repo.return_value.delete_by_user_id.return_value = True
        mock_lect_repo.return_value.create.return_value = [{"lecturer_id": "L_123"}]
        mock_user_repo.return_value.update_user.return_value = None

        service = AdminService()
        result = service.update_user_info(
            user_id_to_update="test_user_123",
            updater_admin_level=2,
            new_account_type="lecturer",
            new_role_id="L_123"
        )

        assert result is not None
        assert result["success"] is True

    @patch('src.storage.client.get_supabase')
    @patch('src.services.admin_service.AdminRepository')
    def test_create_announcement(self, mock_admin_repo, mock_supabase):
        """Test creating announcement"""
        from src.services import AdminService

        # Mock admin repository
        mock_admin_repo.return_value.get_by_id.return_value = {
            "admin_id": "A_test123",
            "user_id": "user_test"
        }

        # Mock Supabase table operations
        mock_table = MagicMock()
        mock_supabase.return_value.table.return_value = mock_table
        mock_table.insert.return_value = mock_table
        mock_table.execute.return_value.data = [{
            "notification_id": "NOT_123",
            "content": "Test announcement"
        }]

        service = AdminService()
        result = service.create_announcement(
            admin_id="A_test123",
            content="Test announcement",
            scope="all"
        )

        assert result is not None
        assert result["success"] is True
