from src.storage.client import get_supabase

class LecturerRepository:
    def __init__(self):
        self.db = get_supabase()
        self.table = self.db.table("lecturer")

    # Lấy tất cả giảng viên
    def get_all_lecturers(self):
        data = self.table.select("*").execute().data
        return data if data else []

    # Lấy giảng viên theo ID
    def get_by_id(self, lecturer_id: str):
        data = self.table.select("*").eq("lecturer_id", lecturer_id).execute().data
        return data[0] if data else None

    # Lấy giảng viên theo user_id
    def get_by_user_id(self, user_id: str):
        data = self.table.select("*").eq("user_id", user_id).execute().data
        return data[0] if data else None

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
    def __init__(self):
        self.db = get_supabase()
        self.table = self.db.table("lecturer")

    def create(self, data: dict):
        try:
            result = self.table.insert(data).execute()
            return result.data
        except Exception as e:
            print(f"Lỗi Supabase khi tạo lecturer: {e}")
            return None
            
    def delete_by_user_id(self, user_id: str):
        try:
            result = self.table.delete().eq("user_id", user_id).execute()
            return result.data
        except Exception as e:
            print(f"Lỗi Supabase khi xóa lecturer: {e}")
            return None