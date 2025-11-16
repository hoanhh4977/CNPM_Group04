from src.storage.repositories.notification_repository import NotificationRepository

def update_announcement(notification_id, new_content):
    repo = NotificationRepository()
    
    # Chỉ cập nhật nội dung
    update_data = {
        "content": new_content
    }
    
    print(f"Đang gửi yêu cầu cập nhật ID: {notification_id}...")
    
    try:
        result = repo.update_notification(notification_id, update_data)
        if result:
            print("=== Cập nhật thông báo thành công ===")
            print(result)
        else:
            print("--- Cập nhật thất bại (có thể ID không tồn tại) ---")
        return result
    except Exception as e:
        print(f"Lỗi Exception khi cập nhật: {e}")
        return None
# Khối test
if __name__ == "__main__":
    print(">>> TEST CẬP NHẬT THÔNG BÁO <<<")
    notif_id = input("Nhập ID thông báo cần cập nhật: ")
    new_content = input("Nhập NỘI DUNG MỚI: ")
    if notif_id and new_content:
        update_announcement(notif_id, new_content)