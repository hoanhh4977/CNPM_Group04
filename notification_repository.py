from src.storage.client import get_supabase 
class NotificationRepository:
    def __init__(self):
        self.db = get_supabase()
        self.table = self.db.table("notification")

    def create_notification(self, data: dict):
        try:
            result = self.table.insert(data).execute()
            return result.data
        except Exception as e:
            print(f"Lỗi Supabase khi tạo thông báo: {e}")
            return None
# (Xem thông báo)
    def get_all_notifications_sorted(self):
        """
        Lấy tất cả thông báo, sắp xếp theo thời gian tạo,
        mới nhất lên đầu (descending).
        """
        try:
            # Sắp xếp theo 'creation_date', mới nhất (desc=True)
            response = self.table.select("*") \
                                 .order("creation_date", desc=True) \
                                 .execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Lỗi Supabase khi lấy danh sách thông báo: {e}")
            return []
    # Xóa
    def delete_notification(self, notification_id):
        """
        Xóa một thông báo dựa trên ID của nó.
        """
        try:
            # Tên cột ID trong DB của bạn là 'notification_id'
            result = self.table.delete() \
                               .eq("notification_id", notification_id) \
                               .execute()
            return result.data
        except Exception as e:
            print(f"Lỗi Supabase khi xóa thông báo: {e}")
            return None
    # Cập nhật
    def update_notification(self, notification_id, update_data: dict):
        """
        Cập nhật thông báo (ví dụ: cột 'content').
        """
        try:
            result = self.table.update(update_data) \
                               .eq("notification_id", notification_id) \
                               .execute()
            return result.data
        except Exception as e:
            print(f"Lỗi Supabase khi cập nhật thông báo: {e}")
            return None