from src.storage.repositories.user_repository import UserRepository 
from src.storage.repositories.admin_repository import AdminRepository 

def delete_user(user_id_to_delete, deleter_admin_level):
    """
    Xóa một user, CÓ KIỂM TRA level admin
    """
    admin_repo = AdminRepository()
    user_repo = UserRepository()
    
    # Lấy level của người BỊ XÓA (target)
    target_admin_details = admin_repo.get_admin_details_by_user_id(user_id_to_delete)
    
    target_level = 0 # Mặc định là 0 (user thường)
    if target_admin_details:
        target_level = target_admin_details['admin_level']
        
    print(f"Level của bạn: {deleter_admin_level}. Level của mục tiêu: {target_level}.")

    # KIỂM TRA QUYỀN
    if deleter_admin_level > target_level:
        # BẠN CÓ QUYỀN
        print(f"Bạn có quyền xóa. Đang xóa user_id: {user_id_to_delete}...")
        try:
            # Lưu ý: Khi xóa user, phải xóa ở cả 2 bảng 
            # (bảng 'administrator' và bảng 'User')
            
            # (Tạm thời chỉ xóa ở bảng 'User')
            result = user_repo.delete_user(user_id_to_delete)
            
            if result:
                print("=== Xóa thành công (từ bảng User) ===")
                # (Bạn cần thêm code để xóa cả trong bảng 'administrator')
            else:
                print("--- Xóa thất bại (Không tìm thấy user trong bảng User) ---")
        except Exception as e:
            print(f"Lỗi Exception khi xóa: {e}")
            
    else:
        print("--- THẤT BẠI: KHÔNG CÓ QUYỀN ---")
        print("Bạn không thể xóa Admin có level BẰNG hoặc CAO HƠN bạn.")

# Khối test
if __name__ == "__main__":
    print(">>> TEST RIÊNG FILE DELETE USER (CÓ CHECK LEVEL) <<<")
    
    my_level = 3 # Giả lập Admin Level 3
    print(f"Bạn đang test với tư cách Admin Level {my_level}")
    
    uid_test = input("Nhập user_ID cần xóa để test: ")
    if uid_test:
        delete_user(uid_test, my_level)