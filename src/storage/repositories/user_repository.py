from src.storage.client import get_supabase

class UserRepository:
    def __init__(self):
        self.db = get_supabase()
        self.table = self.db.table("User")

    # Lấy tất cả người dùng
    def get_all_user(self):
        data = self.table.select("*").execute().data    
        return data if data else []

    # Lấy người dùng theo ID
    def get_user_by_id(self, user_id: str):
        data = self.table.select("*").eq("user_id", user_id).execute().data
        return data[0] if data else None
    
    def get_user_by_username(self, username: str):
        data = self.table.select("*").eq("username", username).execute().data
        return data[0] if data else None

    def get_user_by_phone(self, phone_number: str):
        data = self.table.select("*").eq("phone_number", phone_number).execute().data
        return data[0] if data else None

    # Tạo mới người dùng
    def create_user(self, user_data: dict):
        """
        user_data là dictionary có các field:
        {
            "user_id": "U001",
            "full_name": "Nguyễn Văn A",
            "account_type": "student",
            "password_hash": "hash123",
            "phone_number": "0905123456",
            "address": "TP.HCM"
        }
        """
        result = self.table.insert(user_data).execute()
        return result.data

    # Cập nhật thông tin người dùng
    def update_user(self, user_id: str, update_data: dict):
        result = self.table.update(update_data).eq("user_id", user_id).execute()
        return result.data

    # Xóa người dùng
    def delete_user(self, user_id: str):
        result = self.table.delete().eq("user_id", user_id).execute()
        return result.data
