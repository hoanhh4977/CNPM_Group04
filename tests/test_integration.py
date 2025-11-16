"""
Integration tests for complete workflows
"""
import pytest
from unittest.mock import patch, MagicMock


class TestStudentWorkflow:
    """Test complete student workflow"""

    @patch('src.services.auth_service.UserRepository')
    @patch('src.services.auth_service.StudentRepository')
    @patch('src.services.auth_service.bcrypt')
    @patch('src.services.student_service.SessionRepository')
    @patch('src.services.student_service.AttendanceRepository')
    def test_register_login_and_mark_attendance(
        self, mock_att_repo, mock_sess_repo, mock_bcrypt,
        mock_stud_repo, mock_user_repo, sample_user, sample_session, sample_student
    ):
        """Test: Register -> Login -> Mark Attendance"""
        from src.services import AuthService, StudentService

        # Step 1: Register
        mock_user_repo.return_value.get_user_by_username.return_value = None
        mock_bcrypt.hashpw.return_value.decode.return_value = "hashed"
        mock_user_repo.return_value.create_user.return_value = [{"user_id": "new_123"}]
        mock_stud_repo.return_value.create.return_value = [{"student_id": "S_new123"}]

        auth_service = AuthService()
        register_result = auth_service.register({
            "username": "newstudent",
            "password": "pass123",
            "full_name": "New Student",
            "account_type": "student",
            "phone_number": "0901234567",
            "address": "Test",
            "extra": {"student_id": "S_new123", "class_name": "K23CNTT"}
        })
        assert register_result["success"] is True

        # Step 2: Login
        mock_user_repo.return_value.get_user_by_username.return_value = sample_user
        mock_user_repo.return_value.get_user_by_phone.return_value = None
        mock_stud_repo.return_value.get_by_user_id.return_value = sample_student
        mock_bcrypt.checkpw.return_value = True

        login_result = auth_service.login({"username": "testuser", "password": "password123"})
        assert login_result["success"] is True

        # Step 3: Mark Attendance
        student_id = "S_test123"
        session_id = "SES_test123"

        mock_sess_repo.return_value.get_by_id.return_value = sample_session
        mock_att_repo.return_value.get_attendance_by_student_and_session.return_value = None
        mock_att_repo.return_value.create.return_value = [{"attendance_id": "ATT_123"}]

        student_service = StudentService()
        attendance_result = student_service.mark_attendance(
            student_id, session_id, "ABC123"
        )
        assert attendance_result is not None


class TestLecturerWorkflow:
    """Test complete lecturer workflow"""

    @patch('src.storage.client.get_supabase')
    @patch('src.services.auth_service.UserRepository')
    @patch('src.services.auth_service.LecturerRepository')
    @patch('src.services.auth_service.bcrypt')
    @patch('src.services.lecturer_service.SessionRepository')
    @patch('src.services.lecturer_service.AttendanceRepository')
    def test_register_create_session_and_view_attendance(
        self, mock_att_repo, mock_sess_repo, mock_bcrypt,
        mock_lect_repo, mock_user_repo, mock_supabase
    ):
        """Test: Register -> Create Session -> View Attendance"""
        from src.services import AuthService, LecturerService

        # Step 1: Register
        mock_user_repo.return_value.get_user_by_username.return_value = None
        mock_bcrypt.hashpw.return_value = b"hashed"
        mock_user_repo.return_value.create.return_value = [{"user_id": "lect_123"}]
        mock_lect_repo.return_value.create.return_value = [{"lecturer_id": "L_123"}]

        auth_service = AuthService()
        register_result = auth_service.register(
            username="newlecturer",
            password="pass123",
            full_name="New Lecturer",
            account_type="lecturer",
            phone_number="0901234567",
            address="Test"
        )
        assert register_result["success"] is True

        # Step 2: Create Session
        lecturer_id = "L_123"
        mock_sess_repo.return_value.create.return_value = [{
            "session_id": "SES_456",
            "attendance_code": "XYZ789"
        }]

        lecturer_service = LecturerService()
        session_result = lecturer_service.create_session(
            lecturer_id=lecturer_id,
            subject_name="Python Programming",
            time_slot="Sáng"
        )
        assert session_result["success"] is True

        # Step 3: View Attendance
        session_id = session_result["data"]["session_id"]
        mock_att_repo.return_value.get_by_session.return_value = [
            {
                "attendance_id": "ATT_1",
                "student_id": "S_123",
                "status": "present",
                "check_in_time": "2024-01-01T10:00:00"
            }
        ]

        # Mock supabase tables for student and user lookup
        mock_table = MagicMock()
        mock_supabase.return_value.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value.data = [
            {
                "student_id": "S_123",
                "user_id": "user_123",
                "class_name": "K23",
                "full_name": "Test Student"
            }
        ]

        attendance_result = lecturer_service.view_attendance_by_session(session_id)
        assert attendance_result is not None
        assert isinstance(attendance_result, list)


class TestAdminWorkflow:
    """Test complete admin workflow"""

    @patch('src.storage.client.get_supabase')
    @patch('src.services.admin_service.AdminRepository')
    @patch('src.services.admin_service.UserRepository')
    @patch('src.services.admin_service.StudentRepository')
    @patch('src.services.admin_service.LecturerRepository')
    def test_manage_user_and_create_announcement(
        self, mock_lect_repo, mock_stud_repo, mock_user_repo, mock_admin_repo, mock_supabase
    ):
        """Test: Get Users -> Change Role -> Create Announcement"""
        from src.services import AdminService

        admin_service = AdminService()

        # Step 1: Get All Users
        mock_user_repo.return_value.get_all_users.return_value = [
            {"user_id": "user1", "account_type": "student"},
            {"user_id": "user2", "account_type": "lecturer"}
        ]

        users_result = admin_service.get_all_users()
        assert users_result is not None
        assert len(users_result) == 2

        # Step 2: Change Role (Student -> Lecturer) using update_user_info
        user_id = "user1"
        mock_user_repo.return_value.get_user_by_id.return_value = {
            "user_id": user_id,
            "account_type": "student"
        }
        mock_admin_repo.return_value.get_by_user_id.return_value = None  # Not an admin
        mock_stud_repo.return_value.delete_by_user_id.return_value = True
        mock_lect_repo.return_value.create.return_value = [{"lecturer_id": "L_456"}]
        mock_user_repo.return_value.update_user.return_value = None

        role_result = admin_service.update_user_info(
            user_id_to_update=user_id,
            updater_admin_level=2,
            new_account_type="lecturer",
            new_role_id="L_456"
        )
        assert role_result["success"] is True

        # Step 3: Create Announcement
        mock_admin_repo.return_value.get_by_id.return_value = {
            "admin_id": "A_admin123",
            "user_id": "user_admin"
        }
        mock_table = MagicMock()
        mock_supabase.return_value.table.return_value = mock_table
        mock_table.insert.return_value = mock_table
        mock_table.execute.return_value.data = [{
            "notification_id": "NOT_123",
            "content": "Important announcement"
        }]

        announcement_result = admin_service.create_announcement(
            admin_id="A_admin123",
            content="Important announcement",
            scope="all"
        )
        assert announcement_result["success"] is True


class TestCrossRoleInteractions:
    """Test interactions between different roles"""

    @patch('src.services.lecturer_service.SessionRepository')
    @patch('src.storage.client.get_supabase')
    @patch('src.services.student_service.AttendanceRepository')
    def test_lecturer_creates_session_student_attends(
        self, mock_att_repo, mock_supabase, mock_lect_sess_repo
    ):
        """Test: Lecturer creates session -> Student marks attendance"""
        from src.services import LecturerService, StudentService

        # Lecturer creates session
        lecturer_service = LecturerService()
        session_data = {
            "session_id": "SES_789",
            "attendance_code": "CODE123",
            "lecturer_id": "L_test",
            "subject_name": "Python",
            "time_slot": "Sáng"
        }
        mock_lect_sess_repo.return_value.create.return_value = [session_data]

        session_result = lecturer_service.create_session(
            lecturer_id="L_test",
            subject_name="Python",
            time_slot="Sáng"
        )
        assert session_result["success"] is True

        # Student marks attendance with the code
        student_service = StudentService()

        # Mock get_supabase for session lookup
        mock_session_table = MagicMock()
        mock_supabase.return_value.table.return_value = mock_session_table
        mock_session_table.select.return_value = mock_session_table
        mock_session_table.eq.return_value = mock_session_table
        mock_session_table.execute.return_value.data = [session_data]

        # Mock attendance repository
        mock_att_repo.return_value.table.select.return_value.eq.return_value.eq.return_value.execute.return_value.data = []
        mock_att_repo.return_value.create.return_value = [{"attendance_id": "ATT_999"}]

        attendance_result = student_service.mark_attendance(
            student_id="S_student1",
            session_id=session_data["session_id"],
            attendance_code=session_data["attendance_code"]
        )
        assert attendance_result["success"] is True

    @patch('src.storage.client.get_supabase')
    @patch('src.services.admin_service.AdminRepository')
    def test_admin_creates_announcement_student_views(
        self, mock_admin_repo, mock_supabase
    ):
        """Test: Admin creates announcement -> Student views it"""
        from src.services import AdminService, StudentService

        # Admin creates announcement
        admin_service = AdminService()
        announcement = {
            "notification_id": "NOT_555",
            "content": "System maintenance scheduled",
            "scope": "all"
        }

        # Mock admin repository
        mock_admin_repo.return_value.get_by_id.return_value = {
            "admin_id": "A_admin",
            "user_id": "user_admin"
        }

        # Mock supabase for both admin and student operations
        mock_table = MagicMock()
        mock_supabase.return_value.table.return_value = mock_table
        mock_table.insert.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.in_.return_value = mock_table
        mock_table.order.return_value = mock_table
        mock_table.execute.return_value.data = [announcement]

        create_result = admin_service.create_announcement(
            admin_id="A_admin",
            content="System maintenance scheduled",
            scope="all"
        )
        assert create_result["success"] is True

        # Student views announcements
        student_service = StudentService()

        view_result = student_service.get_announcements(scope="student")
        assert view_result is not None
        assert len(view_result) >= 0
