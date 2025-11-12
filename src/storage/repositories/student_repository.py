from src.storage.client import get_supabase

class StudentRepository:
    def __init__(self):
        self.db = get_supabase()
        self.table = self.db.table("student")

    # Lấy tất cả sinh viên
    def get_all_students(self):
        data = self.table.select("*").execute().data
        return data if data else []

    # Lấy sinh viên theo ID
    def get_by_id(self, student_id: str):
        data = self.table.select("*").eq("student_id", student_id).execute().data
        return data[0] if data else None

    # Lấy sinh viên theo user_id
    def get_by_user_id(self, user_id: str):
        data = self.table.select("*").eq("user_id", user_id).execute().data
        return data[0] if data else None

    # Tạo mới sinh viên
    def create(self, student_data: dict):
        """
        student_data = {
            "student_id": "S001",
            "user_id": "U001",
            "class_name": "K23CNTT"
        }
        """
        result = self.table.insert(student_data).execute()
        return result.data

    # Cập nhật sinh viên
    def update(self, student_id: str, update_data: dict):
        result = self.table.update(update_data).eq("student_id", student_id).execute()
        return result.data

    # Xóa sinh viên
    def delete(self, student_id: str):
        result = self.table.delete().eq("student_id", student_id).execute()
        return result.data
