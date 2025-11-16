from src.storage.repositories.user_repository import UserRepository 
from src.storage.repositories.admin_repository import AdminRepository 

def update_user_info(user_id_to_update, updater_admin_level, phone=None, address=None, password=None):
    """
    Cập nhật thông tin user, CÓ KIỂM TRA level admin
    (Đã sửa lại: check tồn tại trước)
    """
    admin_repo = AdminRepository()
    user_repo = UserRepository()

    # Kiểm tra xem có gì để cập nhật không
    update_data = {}
    if phone:
        update_data["phone_number"] = phone
    if address:
        update_data["address"] = address
    if password:
        update_data["password_hash"] = password 

    if not update_data:
        print("Không có thông tin nào mới để cập nhật.")
        return 

    # KIỂM TRA TỒN TẠI TRƯỚC 
    #  đảm bảo user_repository.py có hàm get_user_by_id
    user_to_update = user_repo.get_user_by_id(user_id_to_update)
    
    if not user_to_update:
        print(f"--- THẤT BẠI: Không tìm thấy user nào có ID: '{user_id_to_update}' ---")
        return # Dừng lại ngay nếu user không tồn tại

    #KIỂM TRA LEVEL ad
    target_admin_details = admin_repo.get_admin_details_by_user_id(user_id_to_update)
    
    target_level = 0
    if target_admin_details:
        target_level = target_admin_details['admin_level']
        
    print(f"Level của bạn: {updater_admin_level}. Level của mục tiêu: {target_level}.")

    # KIỂM TRA QUYỀN
    if updater_admin_level > target_level:
        # try/except
        print(f"Bạn có quyền cập nhật. Đang cập nhật user_id: {user_id_to_update}...")
        try:
            result = user_repo.update_user(user_id_to_update, update_data)
            if result:
                print("=== Cập nhật thành công ===")
                print(result)
            else:
                # Lỗi này không nên xảy ra nữa, nhưng để dự phòng
                print("--- Cập nhật thất bại (Lỗi không rõ) ---")
        except Exception as e:
            print(f"Lỗi Exception khi cập nhật: {e}")
    else:
        print("--- THẤT BẠI: KHÔNG CÓ QUYỀN ---")
        print("Bạn không thể cập nhật thông tin Admin có level BẰNG hoặc CAO HƠN bạn.")
 # Khối test
if __name__ == "__main__":
    print(">>> TEST RIÊNG FILE UPDATE USER (CÓ CHECK LEVEL) <<<")
    
    my_level = 3 # Giả lập Admin Level 3
    print(f"Bạn đang test với tư cách Admin Level {my_level}")
    
    uid_test = input("Nhập user_ID cần cập nhật để test: ")
    new_phone = input("Nhập SĐT mới (bỏ trống để bỏ qua): ")
    
    if uid_test:
        update_user_info(
            user_id_to_update=uid_test,
            updater_admin_level=my_level,
            phone=new_phone
        )