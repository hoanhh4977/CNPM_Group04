from src.storage.repositories.notification_repository import NotificationRepository
import datetime

def show_all_announcements():
    repo = NotificationRepository()
    
    print("Đang lấy danh sách thông báo...")
    notifications = repo.get_all_notifications_sorted() 
    
    if not notifications:
        print("Không có thông báo nào.")
        return

    print("--- TẤT CẢ THÔNG BÁO (Mới nhất lên đầu) ---")
    for notif in notifications:
        notif_id = notif.get('notification_id', '???') # Lấy ID
        # Lấy thông tin cũ
        creator = notif.get('creator_id', 'N/A')
        scope = notif.get('scope', 'N/A')
        content = notif.get('content', '')
        
        try:
            date_str = notif.get('creation_date')
            if date_str:
                dt = datetime.datetime.fromisoformat(date_str)
                time_display = dt.strftime("%d/%m/%Y %H:%M:%S")
            else:
                time_display = "Không rõ"
        except Exception:
            time_display = "Định dạng lỗi"

        print("---------------------------------")
        # Thêm ID
        print(f"== ID THÔNG BÁO: {notif_id} ==") 
        print(f"[{time_display}] - [Người tạo: {creator}] - [Scope: {scope}]")
        print(f"Nội dung: {content}")
        
    print("---------------------------------")

# Khối test
if __name__ == "__main__":
    show_all_announcements()