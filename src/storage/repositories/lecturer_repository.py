from src.storage.client import get_supabase

class LecturerRepository:
    def __init__(self):
        self.db = get_supabase()
        self.table = self.db.table("lecturer")

    def create(self, data):
        return self.table.insert(data).execute().data
        
    # Lấy tất cả giảng viên
    def get_all(self):
        return self.table.select("*").execute().data or []
    # Lấy giảng viên theo ID
    def get_by_id(self, lecturer_id):
        data = self.table.select("*").eq("lecturer_id", lecturer_id).execute().data
        return data[0] if data else None
    
    # Lấy giảng viên theo user_id
    def get_by_user_id(self, user_id):
        return self.table.select("*").eq("user_id", user_id).execute().data or []

    # Tạo mới giảng viên
    def create(self, lecturer_data: dict):
        """
        lecturer_data = {
            "lecturer_id": "L001",
            "user_id": "U001"
        }
        """
        result = self.table.insert(lecturer_data).execute()
        return result.data

    # Cập nhật giảng viên
    def update(self, lecturer_id: str, update_data: dict):
        result = self.table.update(update_data).eq("lecturer_id", lecturer_id).execute()
        return result.data

    # Xóa giảng viên
    def delete(self, lecturer_id: str):
        result = self.table.delete().eq("lecturer_id", lecturer_id).execute()
        return result.data
