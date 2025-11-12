from typing import Dict
import bcrypt

from src.storage.repositories import (
    UserRepository,
    StudentRepository,
    LecturerRepository,
    AdminRepository,
)


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.student_repo = StudentRepository()
        self.lecturer_repo = LecturerRepository()
        self.admin_repo = AdminRepository()

    def login(self, credentials: Dict):
        """
        credentials = {
            "id": "",
            "password": ""
        }
        """

        user = self.user_repo.get_user_by_id(credentials["id"])
        if not user:
            return {"success": False, "error": "User not found"}

        # Verify password
        if not bcrypt.checkpw(credentials["password"].encode('utf-8'), user.password_hash.encode('utf-8')):
            return {"success": False, "error": "Invalid password"}

        # Determine role and attach role-specific info
        role = user.account_type
        extra_data = {}

        if role == "student":
            student = self.student_repo.get_by_user_id(user.user_id)
            if student:
                extra_data = {
                    "student_id": student.student_id,
                    "class_name": student.class_name
                }
        elif role == "lecturer":
            lecturer = self.lecturer_repo.get_by_user_id(user.user_id)
            if lecturer:
                extra_data = {"lecturer_id": lecturer.lecturer_id}
        elif role == "admin":
            admin = self.admin_repo.get_by_user_id(user.user_id)
            if admin:
                extra_data = {
                    "admin_id": admin.admin_id,
                    "admin_level": admin.admin_level
                }

        return {
            "success": True,
            "data": {
                "user_id": user.user_id,
                "full_name": user.full_name,
                "phone_number": user.phone_number,
                "address": user.address,
                "account_type": role,
                **extra_data
            }
        }

    def register(self, user_data: Dict):
        """
        user_data = {
            "user_id": "",
            "full_name": "",
            "password": "",
            "phone_number": "",
            "address": "",
            "account_type": "student"|"lecturer"|"admin",
            "extra": { ... }  # role-specific fields
        }
        """
        # Check if user already exists
        existing = self.user_repo.get_by_id(user_data["user_id"])
        if existing:
            return {"success": False, "error": "User already exists"}

        # Hash password
        hashed_pw = bcrypt.hashpw(user_data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Create user
        self.user_repo.create({
            "user_id": user_data["user_id"],
            "full_name": user_data["full_name"],
            "account_type": user_data["account_type"],
            "password_hash": hashed_pw,
            "phone_number": user_data["phone_number"],
            "address": user_data["address"]
        })

        # Create role-specific record
        role = user_data["account_type"]
        extra = user_data.get("extra", {})

        if role == "student":
            self.student_repo.create({
                "student_id": extra.get("student_id"),
                "user_id": user_data["user_id"],
                "class_name": extra.get("class_name")
            })
        elif role == "lecturer":
            self.lecturer_repo.create({
                "lecturer_id": extra.get("lecturer_id"),
                "user_id": user_data["user_id"]
            })
        elif role == "admin":
            self.admin_repo.create({
                "admin_id": extra.get("admin_id"),
                "user_id": user_data["user_id"],
                "admin_level": extra.get("admin_level", 1)
            })

        return {"success": True, "message": f"{role.capitalize()} registered successfully"}
