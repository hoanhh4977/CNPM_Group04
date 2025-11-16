"""
Admin Service - Nghiệp vụ của Quản trị viên
Chứa tất cả các chức năng quản trị hệ thống
"""

from datetime import datetime
import pytz
from src.storage.repositories import (
    UserRepository,
    AdminRepository,
    StudentRepository,
    LecturerRepository
)
from src.utils.id_generator import generate_notification_id


class AdminService:
    def __init__(self):
        """Khởi tạo các repository cần thiết"""
        self.user_repo = UserRepository()
        self.admin_repo = AdminRepository()
        self.student_repo = StudentRepository()
        self.lecturer_repo = LecturerRepository()

    # ===================== QUẢN LÝ NGƯỜI DÙNG =====================

    def get_all_users(self):
        """
        Lấy danh sách tất cả người dùng

        Trả về:
            list: Danh sách user
        """
        return self.user_repo.get_all_users()

    def update_user_info(self, user_id_to_update: str, updater_admin_level: int,
                        phone: str = None, address: str = None,
                        new_account_type: str = None, new_role_id: str = None):
        """
        Cập nhật thông tin user (có thể bao gồm đổi vai trò)

        Tham số:
            user_id_to_update: ID user cần cập nhật
            updater_admin_level: Level của admin đang thực hiện
            phone: SĐT mới (optional)
            address: Địa chỉ mới (optional)
            new_account_type: Loại tài khoản mới (student/lecturer) (optional)
            new_role_id: ID vai trò mới khi đổi vai trò (optional)

        Trả về:
            dict: {
                "success": True/False,
                "message": "Thông báo"
            }
        """
        # Kiểm tra user tồn tại
        user = self.user_repo.get_user_by_id(user_id_to_update)
        if not user:
            return {
                "success": False,
                "message": f"Không tìm thấy user ID: {user_id_to_update}"
            }

        # Kiểm tra quyền admin
        target_admin = self.admin_repo.get_by_user_id(user_id_to_update)
        target_level = 0
        if target_admin:
            target_level = target_admin.get("admin_level", 0)

        if updater_admin_level <= target_level:
            return {
                "success": False,
                "message": "Bạn không có quyền cập nhật Admin có level bằng hoặc cao hơn bạn!"
            }

        # Cập nhật thông tin đơn giản (SĐT, địa chỉ)
        simple_updates = {}
        if phone:
            simple_updates["phone_number"] = phone
        if address:
            simple_updates["address"] = address

        if simple_updates:
            try:
                self.user_repo.update_user(user_id_to_update, simple_updates)
            except Exception as e:
                return {
                    "success": False,
                    "message": f"Lỗi khi cập nhật thông tin: {str(e)}"
                }

        # Xử lý đổi vai trò (nếu có)
        current_type = user.get("account_type")
        if new_account_type and new_account_type != current_type:
            try:
                # Xóa vai trò cũ
                if current_type == "student":
                    self.student_repo.delete_by_user_id(user_id_to_update)
                elif current_type == "lecturer":
                    self.lecturer_repo.delete_by_user_id(user_id_to_update)

                # Thêm vai trò mới
                if new_account_type == "student":
                    if not new_role_id:
                        return {
                            "success": False,
                            "message": "Phải nhập Student ID mới khi đổi sang Student!"
                        }
                    self.student_repo.create({
                        "student_id": new_role_id,
                        "user_id": user_id_to_update,
                        "class_name": ""
                    })
                elif new_account_type == "lecturer":
                    if not new_role_id:
                        return {
                            "success": False,
                            "message": "Phải nhập Lecturer ID mới khi đổi sang Lecturer!"
                        }
                    self.lecturer_repo.create({
                        "lecturer_id": new_role_id,
                        "user_id": user_id_to_update
                    })

                # Cập nhật account_type trong User
                self.user_repo.update_user(user_id_to_update, {
                    "account_type": new_account_type
                })

                return {
                    "success": True,
                    "message": f"Đã đổi vai trò từ '{current_type}' sang '{new_account_type}' thành công!"
                }
            except Exception as e:
                return {
                    "success": False,
                    "message": f"Lỗi khi đổi vai trò: {str(e)}"
                }

        return {
            "success": True,
            "message": "Cập nhật thông tin thành công!"
        }

    def delete_user(self, user_id_to_delete: str, deleter_admin_level: int):
        """
        Xóa user

        Tham số:
            user_id_to_delete: ID user cần xóa
            deleter_admin_level: Level của admin đang thực hiện

        Trả về:
            dict: {
                "success": True/False,
                "message": "Thông báo"
            }
        """
        # Kiểm tra quyền
        target_admin = self.admin_repo.get_by_user_id(user_id_to_delete)
        target_level = 0
        if target_admin:
            target_level = target_admin.get("admin_level", 0)

        if deleter_admin_level <= target_level:
            return {
                "success": False,
                "message": "Bạn không có quyền xóa Admin có level bằng hoặc cao hơn bạn!"
            }

        # Xóa user
        try:
            # Lấy thông tin user để biết loại
            user = self.user_repo.get_user_by_id(user_id_to_delete)
            if not user:
                return {
                    "success": False,
                    "message": "Không tìm thấy user!"
                }

            account_type = user.get("account_type")

            # Xóa trong bảng role tương ứng
            if account_type == "student":
                self.student_repo.delete_by_user_id(user_id_to_delete)
            elif account_type == "lecturer":
                self.lecturer_repo.delete_by_user_id(user_id_to_delete)
            elif account_type == "admin":
                admin = self.admin_repo.get_by_user_id(user_id_to_delete)
                if admin:
                    self.admin_repo.delete(admin.get("admin_id"))

            # Xóa user
            self.user_repo.delete_user(user_id_to_delete)

            return {
                "success": True,
                "message": "Xóa user thành công!"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi khi xóa user: {str(e)}"
            }

    # ===================== QUẢN LÝ THÔNG BÁO =====================

    def create_announcement(self, admin_id: str, content: str, scope: str):
        """
        Tạo thông báo hệ thống

        Tham số:
            admin_id: ID admin tạo
            content: Nội dung
            scope: Phạm vi (all/student/lecturer)

        Trả về:
            dict: {
                "success": True/False,
                "message": "Thông báo"
            }
        """
        # Lấy user_id từ admin_id
        admin = self.admin_repo.get_by_id(admin_id)
        if not admin:
            return {
                "success": False,
                "message": "Không tìm thấy thông tin admin!"
            }

        creator_id = admin.get("user_id")

        from src.storage.client import get_supabase
        notification_table = get_supabase().table("notification")

        VN_TIMEZONE = pytz.timezone("Asia/Ho_Chi_Minh")
        notification_data = {
            "notification_id": generate_notification_id(),
            "creator_id": creator_id,
            "content": content,
            "scope": scope,
            "creation_date": datetime.now(VN_TIMEZONE).isoformat()
        }

        try:
            notification_table.insert(notification_data).execute()
            return {
                "success": True,
                "message": "Tạo thông báo thành công!"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi khi tạo thông báo: {str(e)}"
            }

    def get_all_announcements(self):
        """
        Lấy tất cả thông báo

        Trả về:
            list: Danh sách thông báo
        """
        from src.storage.client import get_supabase
        notification_table = get_supabase().table("notification")

        notifications = notification_table.select("*")\
            .order("creation_date", desc=True)\
            .execute().data

        return notifications if notifications else []

    def update_announcement(self, notification_id: str, new_content: str):
        """
        Cập nhật thông báo

        Tham số:
            notification_id: ID thông báo
            new_content: Nội dung mới

        Trả về:
            dict: {
                "success": True/False,
                "message": "Thông báo"
            }
        """
        from src.storage.client import get_supabase
        notification_table = get_supabase().table("notification")

        try:
            result = notification_table.update({"content": new_content})\
                .eq("notification_id", notification_id)\
                .execute().data

            if result:
                return {
                    "success": True,
                    "message": "Cập nhật thông báo thành công!"
                }
            else:
                return {
                    "success": False,
                    "message": "Không tìm thấy thông báo!"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi khi cập nhật: {str(e)}"
            }

    def delete_announcement(self, notification_id: str):
        """
        Xóa thông báo

        Tham số:
            notification_id: ID thông báo

        Trả về:
            dict: {
                "success": True/False,
                "message": "Thông báo"
            }
        """
        from src.storage.client import get_supabase
        notification_table = get_supabase().table("notification")

        try:
            result = notification_table.delete()\
                .eq("notification_id", notification_id)\
                .execute().data

            if result:
                return {
                    "success": True,
                    "message": "Xóa thông báo thành công!"
                }
            else:
                return {
                    "success": False,
                    "message": "Không tìm thấy thông báo!"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi khi xóa: {str(e)}"
            }

    # ===================== THỐNG KÊ =====================

    def get_system_statistics(self):
        """
        Lấy thống kê tổng quan hệ thống

        Trả về:
            dict: Các thống kê
        """
        from src.storage.client import get_supabase
        db = get_supabase()

        stats = {
            "total_users": len(self.user_repo.get_all_users()),
            "total_students": len(db.table("student").select("*").execute().data or []),
            "total_lecturers": len(db.table("lecturer").select("*").execute().data or []),
            "total_admins": len(db.table("administrator").select("*").execute().data or []),
            "total_sessions": len(db.table("session").select("*").execute().data or []),
            "total_attendances": len(db.table("attendance").select("*").execute().data or []),
            "total_announcements": len(db.table("notification").select("*").execute().data or [])
        }

        return stats
