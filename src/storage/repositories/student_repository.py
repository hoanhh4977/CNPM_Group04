from src.storage.client import get_supabase

class StudentRepository:
    def __init__(self):
        self.db = get_supabase()
        self.table = self.db.table("student")

    def create(self, student_data: dict):
        """
        Tạo sinh viên mới
        student_data = {
            "student_id": "S001",
            "user_id": "U001",
            "class_name": "K23CNTT"
        }
        """
        try:
            result = self.table.insert(student_data).execute()
            return result.data
        except Exception as e:
            print(f"Lỗi Supabase khi tạo student: {e}")
            return None

    def get_all(self):
        """Lấy tất cả sinh viên"""
        data = self.table.select("*").execute().data
        return data if data else []

    def get_by_id(self, student_id: str):
        """Lấy sinh viên theo ID"""
        data = self.table.select("*").eq("student_id", student_id).execute().data
        return data[0] if data else None

    def get_by_user_id(self, user_id: str):
        """Lấy sinh viên theo user_id"""
        data = self.table.select("*").eq("user_id", user_id).execute().data
        return data[0] if data else None

    def update(self, student_id: str, update_data: dict):
        """Cập nhật sinh viên"""
        result = self.table.update(update_data).eq("student_id", student_id).execute()
        return result.data

    def delete(self, student_id: str):
        """Xóa sinh viên"""
        result = self.table.delete().eq("student_id", student_id).execute()
        return result.data

    def delete_by_user_id(self, user_id: str):
        """Xóa sinh viên theo user_id"""
        try:
            result = self.table.delete().eq("user_id", user_id).execute()
            return result.data
        except Exception as e:
            print(f"Lỗi Supabase khi xóa student: {e}")
            return None
