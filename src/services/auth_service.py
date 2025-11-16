from typing import Dict
import uuid
import bcrypt
import time
import getpass

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
            "username": "",
            "password": ""
        }
        """

        user = self.user_repo.get_user_by_username(credentials["username"])
        user_by_phone = self.user_repo.get_user_by_phone(credentials["username"])
        if not user and not user_by_phone:
            return {"success": False, "error": "Không tìm thấy người dùng"}
        if not user:
            user = user_by_phone

        # Verify password
        if not bcrypt.checkpw(credentials["password"].encode('utf-8'), user["password_hash"].encode('utf-8')):
            return {"success": False, "error": "Mật khẩu không đúng"}

        # Determine role and attach role-specific info
        role = user["account_type"]
        extra_data = {}

        if role == "student":
            student = self.student_repo.get_by_user_id(user["user_id"])
            extra_data = {
                "student_id": student["student_id"],
                "class_name": student["class_name"]
            }
        if role == "lecturer":
            lecturer = self.lecturer_repo.get_by_user_id(user["user_id"])
            extra_data = {
                "lecturer_id": lecturer["lecturer_id"]
            }
        if role == "admin":
            admin = self.admin_repo.get_by_user_id(user["user_id"])
            extra_data = {
                "admin_id": admin["admin_id"],
                "admin_level": admin["admin_level"]
            }

        return {
            "success": True,
            "data": {
                "user_id": user["user_id"],
                "full_name": user["full_name"],
                "phone_number": user["phone_number"],
                "address": user["address"],
                "account_type": role,
                **extra_data
            }
        }

    def register(self, user_data: Dict):
        """
        user_data = {
            "username": "",
            "full_name": "",
            "password": "",
            "phone_number": "",
            "address": "",
            "account_type": "student"|"lecturer"|"admin",
            "extra": { ... }  # role-specific fields
        }
        """
        # Check if user already exists
        existing = self.user_repo.get_user_by_username(user_data["username"])
        if existing:
            return {"success": False, "error": "Người dùng đã tồn tại. Vui lòng chọn tên đăng nhập khác."}

        # Hash password
        hashed_pw = bcrypt.hashpw(user_data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user_id = str(uuid.uuid4())
        # Create user
        self.user_repo.create_user({
            "user_id": user_id,
            "username": user_data["username"],
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
                "user_id": user_id,
                "class_name": extra.get("class_name")
            })
        elif role == "lecturer":
            self.lecturer_repo.create({
                "lecturer_id": extra.get("lecturer_id"),
                "user_id": user_id
            })

        return {"success": True, "message": f"{role.capitalize()} đăng ký thành công!"}

    def console_login(self):
        print("\n" + "="*40)
        print("✨ HỆ THỐNG ĐĂNG NHẬP ✨")
        print("="*40)

        username = input("Tên đăng nhập hoặc số điện thoại: ")
        password = getpass.getpass("Mật khẩu: ")

        print("Đang kiểm tra thông tin...")
        time.sleep(0.5)

        result = self.login({
            "username": username,
            "password": password
        })

        user = None
        if result["success"]:
            print("\n🎉 Đăng nhập thành công!")
            user = result["data"]
            print(f"Xin chào, {user['full_name']} ({user['account_type']})")
        else:
            print("\n❌ Lỗi đăng nhập:", result["error"])

        print("="*40 + "\n")

        return user

    def console_register(self):
        print("\n" + "="*40)
        print("✨ ĐĂNG KÝ TÀI KHOẢN ✨")
        print("="*40)

        username = input("Tên đăng nhập: ")
        full_name = input("Họ và tên: ")
        password = input("Mật khẩu: ")
        # ensure phone_number contain only 10 digits
        while True:
            phone_number = input("Số điện thoại: ")
            if phone_number.isdigit() and len(phone_number) == 10:
                break
            print("❗ Số điện thoại không hợp lệ. Vui lòng nhập đúng 10 chữ số.")
        address = input("Địa chỉ: ")

        print("\nChọn loại tài khoản:")
        print("  1. Sinh viên")
        print("  2. Giảng viên")
        
        while True:
            role_choice = input("Nhập lựa chọn (1/2): ").strip()
            if role_choice in ["1", "2"]:
                break
            print("❗ Lựa chọn không hợp lệ. Hãy chọn 1 hoặc 2.")

        account_type = "student" if role_choice == "1" else "lecturer"

        extra = {}
        if account_type == "student":
            print("\n--- Thông tin sinh viên ---")
            extra["student_id"] = str(uuid.uuid4())
            extra["class_name"] = input("Lớp học: ")
        else:
            print("\n--- Thông tin giảng viên ---")
            extra["lecturer_id"] = str(uuid.uuid4())
        # Xác nhận
        print("\nVui lòng kiểm tra lại thông tin:")
        print(f"- Tên đăng nhập: {username}")
        print(f"- Họ tên: {full_name}")
        print(f"- Vai trò: {account_type}")
        print(f"- Số điện thoại: {phone_number}")
        print(f"- Địa chỉ: {address}")
        for k, v in extra.items():
            print(f"- {k}: {v}")

        confirm = input("Bạn có chắc muốn tạo tài khoản? (y/n): ").lower()
        if confirm != "y":
            print("❌ Huỷ đăng ký.\n")
            return

        print("Đang tạo tài khoản...")
        time.sleep(0.5)

        user_data = {
            "username": username,
            "full_name": full_name,
            "password": password,
            "phone_number": phone_number,
            "address": address,
            "account_type": account_type,
            "extra": extra
        }

        result = self.register(user_data)

        if result["success"]:
            print("\n🎉", result["message"])
        else:
            print("\n❌ Lỗi đăng ký:", result["error"])

        print("="*40 + "\n")

        user = None
        if result["success"]:
            login_result = self.login({
                "username": username,
                "password": password
            })
            if login_result["success"]:
                user = login_result["data"]
        
        return user