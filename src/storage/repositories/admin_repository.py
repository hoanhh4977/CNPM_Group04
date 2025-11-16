from src.storage.client import get_supabase

class AdminRepository:
    def __init__(self):
        self.db = get_supabase()
        self.table = self.db.table("administrator")

    # Lấy tất cả admin
    def get_all_admin(self):
        data = self.table.select("*").execute().data
        return data if data else []

    # Lấy admin theo ID
    def get_by_id(self, admin_id: str):
        data = self.table.select("*").eq("admin_id", admin_id).execute().data
        return data[0] if data else None

    # Lấy admin theo user_id
    def get_by_user_id(self, user_id: str):
        data = self.table.select("*").eq("user_id", user_id).execute().data
        return data[0] if data else None

    # Tạo mới admin
    def create(self, admin_data: dict):
        """
        admin_data = {
            "admin_id": "A001",
            "user_id": "U001",
            "admin_level": 1
        }
        """
        result = self.table.insert(admin_data).execute()
        return result.data

    # Cập nhật admin
    def update(self, admin_id: str, update_data: dict):
        result = self.table.update(update_data).eq("admin_id", admin_id).execute()
        return result.data

    # Xóa admin
    def delete(self, admin_id: str):
        result = self.table.delete().eq("admin_id", admin_id).execute()
        return result.data

