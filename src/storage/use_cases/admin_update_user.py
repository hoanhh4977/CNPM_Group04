# src/storage/use_cases/admin_update_user.py

# Import tất cả các repo cần thiết
from src.storage.repositories.user_repository import UserRepository 
from src.storage.repositories.admin_repository import AdminRepository 
from src.storage.repositories.student_repository import StudentRepository
from src.storage.repositories.lecturer_repository import LecturerRepository

def update_user_info(user_id_to_update, updater_admin_level, 
                     phone=None, address=None, 
                     new_account_type=None, new_role_id=None):
    """
    Cập nhật thông tin user (Logic phức tạp - Đổi vai trò)
    """
    admin_repo = AdminRepository()
    user_repo = UserRepository()
    student_repo = StudentRepository()
    lecturer_repo = LecturerRepository()

    # 1. KIỂM TRA TỒN TẠI
    user_to_update = user_repo.get_user_by_id(user_id_to_update)
    if not user_to_update:
        print(f"--- THẤT BẠI: Không tìm thấy user nào có ID: '{user_id_to_update}' ---")
        return

    # 2. KIỂM TRA LEVEL ADMIN (Quyền)
    target_admin_details = admin_repo.get_by_user_id(user_id_to_update)
    target_level = 0
    if target_admin_details:
        target_level = target_admin_details['admin_level'] 
        
    print(f"Level của bạn: {updater_admin_level}. Level của mục tiêu: {target_level}.")

    if updater_admin_level <= target_level:
        print("--- THẤT BẠI: KHÔNG CÓ QUYỀN ---")
        print("Bạn không thể cập nhật thông tin Admin có level BẰNG hoặc CAO HƠN bạn.")
        return

    # ===============================================
    # BẮT ĐẦU XỬ LÝ CẬP NHẬT
    # ===============================================
    print(f"Bạn có quyền cập nhật user: {user_id_to_update}...")
    
    # -- A. Xử lý các thay đổi đơn giản (SĐT, Địa chỉ) --
    simple_update_data = {}
    if phone:
        simple_update_data["phone_number"] = phone
    if address:
        simple_update_data["address"] = address
        
    if simple_update_data:
        try:
            user_repo.update_user(user_id_to_update, simple_update_data)
            print("Cập nhật SĐT/Địa chỉ thành công.")
        except Exception as e:
            print(f"Lỗi khi cập nhật SĐT/Địa chỉ: {e}")

    # -- B. Xử lý thay đổi vai trò (Phức tạp) --
    current_account_type = user_to_update.get("account_type")
    
    # Chỉ chạy khi 1. Admin nhập vai trò mới, 2. Vai trò đó khác vai trò cũ
    if new_account_type and new_account_type != current_account_type:
        print(f"Đang đổi vai trò từ '{current_account_type}' sang '{new_account_type}'...")
        
        try:
            # B1: Xóa vai trò cũ (nếu có)
            if current_account_type == "student":
                print(f"Xóa {user_id_to_update} khỏi bảng 'student'...")
                student_repo.delete_by_user_id(user_id_to_update)
            elif current_account_type == "lecturer":
                print(f"Xóa {user_id_to_update} khỏi bảng 'lecturer'...")
                lecturer_repo.delete_by_user_id(user_id_to_update)
            
            # B2: Thêm vai trò mới
            if new_account_type == "student":
                if not new_role_id: # Kiểm tra xem admin có nhập ID mới không
                    print("Lỗi: Phải nhập Student ID mới để thêm vai trò 'student'.")
                    return
                print(f"Thêm {user_id_to_update} vào bảng 'student' với ID: {new_role_id}...")
                student_repo.create({"student_id": new_role_id, "user_id": user_id_to_update})
                
            elif new_account_type == "lecturer":
                if not new_role_id:
                    print("Lỗi: Phải nhập Lecturer ID mới để thêm vai trò 'lecturer'.")
                    return
                print(f"Thêm {user_id_to_update} vào bảng 'lecturer' với ID: {new_role_id}...")
                lecturer_repo.create({"lecturer_id": new_role_id, "user_id": user_id_to_update})

            # B3: Cập nhật bảng 'User'
            user_repo.update_user(user_id_to_update, {"account_type": new_account_type})
            
            print("=== Đổi vai trò thành công! ===")

        except Exception as e:
            print(f"--- LỖI NGHIÊM TRỌNG KHI ĐỔI VAI TRÒ: {e} ---")
            print("DỮ LIỆU CÓ THỂ BỊ MẤT ĐỒNG BỘ. VUI LÒNG KIỂM TRA DATABASE.")

    elif not new_account_type:
        print("Không có thay đổi vai trò.")
    else:
        print(f"User đã là '{new_account_type}', không cần đổi.")

# Khối test (Giữ nguyên, chỉ cập nhật tham số)
if __name__ == "__main__":
    print(">>> TEST RIÊNG FILE UPDATE USER (LOGIC PHỨC TẠP) <<<")
    my_level = 3
    print(f"Bạn đang test với tư cách Admin Level {my_level}")
    
    uid_test = input("Nhập user_ID cần cập nhật để test: ")
    new_phone = input("Nhập SĐT mới (bỏ trống): ")
    new_type = input("Nhập LOẠI TK MỚI (student/lecturer) (bỏ trống): ")
    new_rid = input("Nhập ID vai trò mới (S00x/L00x) (bỏ trống): ")
    
    if uid_test:
        update_user_info(
            user_id_to_update=uid_test,
            updater_admin_level=my_level,
            phone=new_phone,
            new_account_type=new_type,
            new_role_id=new_rid
        )