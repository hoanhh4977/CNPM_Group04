from src.storage.repositories.notification_repository import NotificationRepository

def delete_announcement(notification_id):
    repo = NotificationRepository()
    print(f"Đang gửi yêu cầu xóa thông báo ID: {notification_id}...")
    
    try:
        result = repo.delete_notification(notification_id)
        if result:
            print("=== Xóa thông báo thành công ===")
            print(result)
        else:
            print("--- Xóa thất bại (có thể ID không tồn tại) ---")
        return result
    except Exception as e:
        print(f"Lỗi Exception khi xóa: {e}")
        return None
# Khối test
if __name__ == "__main__":
    print(">>> TEST XÓA THÔNG BÁO <<<")
    notif_id = input("Nhập ID thông báo cần xóa: ")
    if notif_id:
        delete_announcement(notif_id)