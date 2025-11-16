"""
Unit tests for repositories
"""
import pytest
from unittest.mock import patch, MagicMock


class TestUserRepository:
    """Test UserRepository"""

    @patch('src.storage.repositories.user_repository.get_supabase')
    def test_get_all_users(self, mock_get_supabase, sample_user):
        """Test getting all users"""
        from src.storage.repositories import UserRepository

        # Setup mock
        mock_client = MagicMock()
        mock_table = MagicMock()
        mock_get_supabase.return_value = mock_client
        mock_client.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[sample_user])

        # Test
        repo = UserRepository()
        users = repo.get_all_users()

        assert len(users) == 1
        assert users[0]["username"] == "testuser"

    @patch('src.storage.repositories.user_repository.get_supabase')
    def test_get_user_by_id(self, mock_get_supabase, sample_user):
        """Test getting user by ID"""
        from src.storage.repositories import UserRepository

        # Setup mock
        mock_client = MagicMock()
        mock_table = MagicMock()
        mock_get_supabase.return_value = mock_client
        mock_client.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[sample_user])

        # Test
        repo = UserRepository()
        user = repo.get_user_by_id("test_user_123")

        assert user is not None
        assert user["user_id"] == "test_user_123"

    @patch('src.storage.repositories.user_repository.get_supabase')
    def test_get_user_by_username(self, mock_get_supabase, sample_user):
        """Test getting user by username"""
        from src.storage.repositories import UserRepository

        mock_client = MagicMock()
        mock_table = MagicMock()
        mock_get_supabase.return_value = mock_client
        mock_client.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[sample_user])

        repo = UserRepository()
        user = repo.get_user_by_username("testuser")

        assert user is not None
        assert user["username"] == "testuser"


class TestStudentRepository:
    """Test StudentRepository"""

    @patch('src.storage.repositories.student_repository.get_supabase')
    def test_get_by_user_id(self, mock_get_supabase, sample_student):
        """Test getting student by user_id"""
        from src.storage.repositories import StudentRepository

        mock_client = MagicMock()
        mock_table = MagicMock()
        mock_get_supabase.return_value = mock_client
        mock_client.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[sample_student])

        repo = StudentRepository()
        student = repo.get_by_user_id("test_user_123")

        assert student is not None
        assert student["class_name"] == "K23CNTT"


class TestSessionRepository:
    """Test SessionRepository"""

    @patch('src.storage.repositories.session_repository.get_supabase')
    def test_create_session(self, mock_get_supabase, sample_session):
        """Test creating a session"""
        from src.storage.repositories import SessionRepository

        mock_client = MagicMock()
        mock_table = MagicMock()
        mock_get_supabase.return_value = mock_client
        mock_client.table.return_value = mock_table
        mock_table.insert.return_value = mock_table
        mock_table.execute.return_value = MagicMock(data=[sample_session])

        repo = SessionRepository()
        result = repo.create(sample_session)

        assert result is not None
        assert len(result) > 0
