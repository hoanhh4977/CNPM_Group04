import datetime
import pytz # Import thư viện múi giờ
from src.storage.repositories.notification_repository import NotificationRepository

# 1. Định nghĩa múi giờ Việt Nam (GMT+7)
VN_TIMEZONE = pytz.timezone("Asia/Ho_Chi_Minh")

def create_new_announcement(content, creator_id, scope):
    """
    Tạo một thông báo mới (phiên bản đầy đủ)
    Nhận vào: 
    - content (nội dung)
    - creator_id (ID người tạo)
    - scope (phạm vi: 'all', 'lecturer', 'student')
    """
    repo = NotificationRepository()
    
    # 2. Lấy giờ Việt Nam hiện tại
    current_time_vn = datetime.datetime.now(VN_TIMEZONE).isoformat()

    # 3. Đóng gói dữ liệu (khớp với 4 cột trong DB)
    announcement_data = {
        "content": content,
        "creator_id": creator_id,
        "scope": scope,
        "creation_date": current_time_vn 
    }
    
    print(f"Đang gửi lên DB: {announcement_data}")
    
    try:
        result = repo.create_notification(announcement_data)
        
        if result: 
            print("=== Tạo thông báo thành công ===")
            print(result)
            return result
        else:
            print("--- Tạo thông báo THẤT BẠI (Lỗi từ repository) ---")
            return None
        
    except Exception as e:
        print(f"Lỗi Exception khi tạo thông báo: {e}")
        return None

# KHỐI TEST
if __name__ == "__main__":
    print(">>> TEST TẠO THÔNG BÁO MỚI (Phiên bản đầy đủ) <<<")
    
    # Test việc hỏi Scope
    print("Vui lòng chọn phạm vi thông báo:")
    print("  1. Gửi cho tất cả (all)")
    print("  2. Gửi cho Giảng viên (lecturer)")
    print("  3. Gửi cho Sinh viên (student)")
    
    scope_map = {"1": "all", "2": "lecturer", "3": "student"}
    
    scope = None
    while scope is None: # Lặp cho đến khi có scope hợp lệ
        scope_choice = input("Lựa chọn (1-3): ")
        scope = scope_map.get(scope_choice) # Lấy giá trị, sẽ là None nếu nhập sai
        
        if scope is None:
            print("Lựa chọn không hợp lệ. Vui lòng nhập lại (1, 2, hoặc 3).")
    
    print(f"Đã chọn scope: {scope}") # In ra scope đã chọn

    # Test việc hỏi Content
    content = ""
    while not content:
        content = input("Nhập nội dung thông báo: ")
        if not content:
            print("Nội dung không được để trống!")
            
    # Test ID người tạo (dùng ID giả)
    creator_id = "admin_test_id_001"
    
    print("--- ĐANG CHẠY TEST ---")
    create_new_announcement(content, creator_id, scope)