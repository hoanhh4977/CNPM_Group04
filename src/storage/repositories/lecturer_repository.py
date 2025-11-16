from src.storage.client import get_supabase

class LecturerRepository:
    def __init__(self):
        self.db = get_supabase()
        self.table = self.db.table("lecturer")

    def create(self, lecturer_data: dict):
        """
        Tạo giảng viên mới
        lecturer_data = {
            "lecturer_id": "L001",
            "user_id": "U001"
        }
        """
        try:
            result = self.table.insert(lecturer_data).execute()
            return result.data
        except Exception as e:
            print(f"Lỗi Supabase khi tạo lecturer: {e}")
            return None

    def get_all(self):
        """Lấy tất cả giảng viên"""
        return self.table.select("*").execute().data or []

    def get_by_id(self, lecturer_id):
        """Lấy giảng viên theo ID"""
        data = self.table.select("*").eq("lecturer_id", lecturer_id).execute().data
        return data[0] if data else None

    def get_by_user_id(self, user_id):
        """Lấy giảng viên theo user_id"""
        data = self.table.select("*").eq("user_id", user_id).execute().data
        return data[0] if data else None

    def update(self, lecturer_id: str, update_data: dict):
        """Cập nhật giảng viên"""
        result = self.table.update(update_data).eq("lecturer_id", lecturer_id).execute()
        return result.data

    def delete(self, lecturer_id: str):
        """Xóa giảng viên"""
        result = self.table.delete().eq("lecturer_id", lecturer_id).execute()
        return result.data

    def delete_by_user_id(self, user_id: str):
        """Xóa giảng viên theo user_id"""
        try:
            result = self.table.delete().eq("user_id", user_id).execute()
            return result.data
        except Exception as e:
            print(f"Lỗi Supabase khi xóa lecturer: {e}")
            return None
