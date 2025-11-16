<<<<<<< HEAD
try:
    from src.storage.use_cases.admin_show_users import show_all_users 
    from src.storage.use_cases.admin_update_user import update_user_info
    from src.storage.use_cases.admin_delete_user import delete_user

    from src.storage.use_cases.admin_create_announcement import create_new_announcement
    from src.storage.use_cases.admin_show_announcements import show_all_announcements
    from src.storage.use_cases.admin_update_announcement import update_announcement
    from src.storage.use_cases.admin_delete_announcement import delete_announcement
    
except ImportError as e:
    print(f"LỖI IMPORT: {e}")
    print("Vui lòng kiểm tra lại các file trong 'src/storage/use_cases/'")
    exit()

#  CÁC HÀM "MENU" CON

def menu_show_users():
    """Hàm này gọi chức năng Hiển thị danh sách"""
    print("\n--- [1] DANH SÁCH NGƯỜI DÙNG ---")
    try:
        show_all_users() 
    except Exception as e:
        print(f"Lỗi khi hiển thị danh sách: {e}")

def menu_update_user(updater_admin_level):
    """Hàm này gọi chức năng Cập nhật (Sửa SĐT, Địa chỉ, Vai trò)"""
    print("\n--- [2] CẬP NHẬT NGƯỜI DÙNG ---")
    try:
        user_id_to_update = ""
        while not user_id_to_update:
            user_id_to_update = input("Nhập user_ID của người dùng bạn muốn sửa: ")
            if not user_id_to_update:
                print("ID không được để trống!")

        print("Nhập thông tin mới (Nếu không muốn đổi, nhấn Enter để bỏ qua):")
        
        # --- Validation SĐT (Giữ nguyên) ---
        while True:
            phone = input(" - Số điện thoại mới: ")
            if not phone:
                break 
            if phone.isdigit() and len(phone) == 10:
                break
            else:
                print("Lỗi: SĐT phải là 10 chữ số. Vui lòng nhập lại (hoặc Enter để bỏ qua).")
        
        address = input(" - Địa chỉ mới: ")
        
        # ===== THAY ĐỔI TỪ MẬT KHẨU SANG VAI TRÒ =====
        new_account_type = ""
        while True:
            new_account_type = input(" - Loại tài khoản mới (student/lecturer): ")
            if not new_account_type:
                break # Người dùng bỏ qua
            if new_account_type in ["student", "lecturer"]:
                break # Hợp lệ
            else:
                print("Lỗi: Chỉ chấp nhận 'student' hoặc 'lecturer' (hoặc Enter để bỏ qua).")
        # ============================================
        
        # Biến để lưu ID vai trò mới (nếu cần)
        new_role_id = None
        if new_account_type == "student":
            new_role_id = input(f"Nhập Student ID MỚI cho user '{user_id_to_update}' (ví dụ: S001): ")
        elif new_account_type == "lecturer":
            new_role_id = input(f"Nhập Lecturer ID MỚI cho user '{user_id_to_update}' (ví dụ: L001): ")

        # Gọi hàm use_case (giờ chuyền thêm new_role_id)
        update_user_info(
            user_id_to_update=user_id_to_update,
            updater_admin_level=updater_admin_level,
            phone=phone,
            address=address,
            new_account_type=new_account_type,
            new_role_id=new_role_id # <-- Chuyền ID vai trò mới
        )
    except Exception as e:
        print(f"Lỗi khi cập nhật: {e}")
def menu_delete_user(deleter_admin_level):
    """Hàm này gọi chức năng Xóa (có kiểm tra level)"""
    print("\n--- [3] XÓA TÀI KHOẢN NGƯỜI DÙNG ---")
    try:
        user_id_to_delete = ""
        while not user_id_to_delete:
            user_id_to_delete = input("Nhập user_ID của người dùng bạn muốn XÓA: ")
        
        confirm = input(f"Bạn có CHẮC CHẮN muốn xóa user '{user_id_to_delete}' không? (gõ 'yes' để xác nhận): ")
        
        if confirm.lower() == 'yes':
            delete_user(
                user_id_to_delete=user_id_to_delete,
                deleter_admin_level=deleter_admin_level
            )
        else:
            print("Đã hủy thao tác xóa.")
    except Exception as e:
        print(f"Lỗi khi xóa: {e}")

def menu_create_announcement(admin_creator_id):
    """Hàm này là 'nút bấm' cho lựa chọn 4."""
    print("\n--- [4] TẠO THÔNG BÁO MỚI ---")
    
    # Lấy Scope 
    scope = None
    scope_map = {"1": "all", "2": "lecturer", "3": "student"}
    while scope is None:
        print("Vui lòng chọn phạm vi thông báo:")
        print("  1. Gửi cho tất cả (all)")
        print("  2. Gửi cho Giảng viên (lecturer)")
        print("  3. Gửi cho Sinh viên (student)")
        print("  (hoặc gõ 'q' để hủy)")
        
        scope_choice = input("Lựa chọn của bạn (1-3, q): ")
        if scope_choice.lower() == 'q':
            print("Đã hủy tạo thông báo.")
            return
        
        scope = scope_map.get(scope_choice)
        if scope is None:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
            
    #  Lấy Content 
    content = ""
    while not content:
        content = input("Nhập nội dung thông báo: ")
        if not content:
            print("Nội dung không được để trống!")
    
    # Gọi Use Case
    try:
        print(f"\nĐang tạo thông báo (Scope: {scope}, Admin: {admin_creator_id})...")
        create_new_announcement(
            content=content,
            creator_id=admin_creator_id,
            scope=scope
        )
    except Exception as e:
        print(f"Lỗi khi tạo thông báo: {e}")

def menu_show_announcements():
    """Hàm này là 'nút bấm' cho lựa chọn 5."""
    print("\n--- [5] XEM TẤT CẢ THÔNG BÁO ---")
    try:
        show_all_announcements()
    except Exception as e:
        print(f"Lỗi khi xem thông báo: {e}")

def menu_update_announcement():
    """Hàm này là 'nút bấm' cho lựa chọn 6 (Cập nhật)"""
    print("\n--- [6] CẬP NHẬT THÔNG BÁO ---")
    print("(Mẹo: Chạy chức năng '5. Xem tất cả thông báo' để lấy ID)")
    
    try:
        notif_id = input("Nhập ID thông báo bạn muốn cập nhật: ")
        if not notif_id:
            print("Đã hủy. ID không được để trống.")
            return

        new_content = input("Nhập NỘI DUNG MỚI (bỏ trống nếu không muốn đổi): ")
        
        if not new_content:
            print("Không có gì để cập nhật. Đã hủy.")
            return
        
        update_announcement(notif_id, new_content)

    except Exception as e:
        print(f"Lỗi khi cập nhật thông báo: {e}")

def menu_delete_announcement():
    """Hàm này là 'nút bấm' cho lựa chọn 7 (Xóa) - Đã cập nhật logic Yes/No"""
    print("\n--- [7] XÓA THÔNG BÁO ---")
    print("(Mẹo: Chạy chức năng '5. Xem tất cả thông báo' để lấy ID)")
    
    try:
        notif_id = input("Nhập ID thông báo bạn muốn XÓA (hoặc 'q' để hủy): ")
        if not notif_id or notif_id.lower() == 'q':
            print("Đã hủy.")
            return

        # Yes/No
        while True:
            confirm = input(f"Bạn có CHẮC CHẮN muốn xóa thông báo ID '{notif_id}' không? (nhập 'yes' hoặc 'no'): ")
            
            if confirm.lower() == 'yes':
                print("\nĐang tiến hành xóa...")
                delete_announcement(notif_id) # Gọi hàm nghiệp vụ
                break 
                
            elif confirm.lower() == 'no':
                print("Đã hủy thao tác xóa.")
                break
                
            else:
                print("Lỗi: Vui lòng chỉ nhập 'yes' (để xóa) hoặc 'no' (để hủy).")
    except Exception as e:
        print(f"Lỗi khi xóa thông báo: {e}")

# HÀM MENU CHÍNH
def run_admin_menu(admin_session):
    """
    admin_session = {"admin_id": "A001", "user_id": "U001", "level": 3}
    """
    current_admin_id = admin_session['admin_id']
    current_admin_level = admin_session['admin_level']
    
    while True:
        print("\n======================================")
        print(f"   ADMIN MENU (ID: {current_admin_id} | Level: {current_admin_level})")
        print("======================================")
        print("--- Quản lý người dùng ---")
        print("1. Hiển thị danh sách người dùng")
        print("2. Chỉnh sửa thông tin người dùng")
        print("3. Xóa tài khoản người dùng")
        print("--- Quản lý thông báo ---")
        print("4. Tạo thông báo mới")
        print("5. Xem tất cả thông báo (ĐỂ LẤY ID)")
        print("6. Cập nhật thông báo (THEO ID)")
        print("7. Xóa thông báo (THEO ID)")
        print("-------------------------")
        print("8. Quay lại (Đăng xuất)")
        print("--------------------------------------")
        
        choice = input("Vui lòng chọn chức năng (1-8): ")
        
        if choice == '1':
            menu_show_users()
        elif choice == '2':
            menu_update_user(current_admin_level) # Chuyền level 
        elif choice == '3':
            menu_delete_user(current_admin_level) # Chuyền level 
        elif choice == '4':
            menu_create_announcement(current_admin_id) # Chuyền ID admin
        elif choice == '5':
            menu_show_announcements()
        elif choice == '6':
            menu_update_announcement() 
        elif choice == '7':
            menu_delete_announcement() 
        elif choice == '8':
            print("Đang đăng xuất...")
            break 
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
        
        input("\nNhấn Enter để quay lại menu admin...")

# KHỐI CHẠY TEST
if __name__ == "__main__":
    print(">>> CHẠY TEST RIÊNG FILE ADMIN_MENU <<<")
    
    test_session = {
        "admin_id": "A_Test_ID", 
        "user_id": "U_Test_ID", 
        "admin_level": 3 
    }
    
=======
try:
    from src.storage.use_cases.admin_show_users import show_all_users 
    from src.storage.use_cases.admin_update_user import update_user_info
    from src.storage.use_cases.admin_delete_user import delete_user
    
    from src.storage.use_cases.admin_create_announcement import create_new_announcement
    from src.storage.use_cases.admin_show_announcements import show_all_announcements
    
    from src.storage.use_cases.admin_update_announcement import update_announcement
    from src.storage.use_cases.admin_delete_announcement import delete_announcement
    
except ImportError as e:
    print(f"LỖI IMPORT: {e}")
    exit()
# CÁC HÀM MENU CON

def menu_show_users():
    """Hàm này gọi chức năng Hiển thị danh sách"""
    print("\n--- [1] DANH SÁCH NGƯỜI DÙNG ---")
    try:
        show_all_users() 
    except Exception as e:
        print(f"Lỗi khi hiển thị danh sách: {e}")

def menu_update_user(updater_admin_level): # NHẬN LEVEL CỦA 
    """Hàm này gọi chức năng Cập nhật (ĐÃ CÓ VALIDATION SĐT)"""
    print("\n--- [2] CẬP NHẬT NGƯỜI DÙNG ---")
    try:
        # Lấy ID của người sửa
        user_id_to_update = ""
        while not user_id_to_update:
            user_id_to_update = input("Nhập user_ID của người dùng bạn muốn sửa: ")
            if not user_id_to_update:
                print("ID không được để trống!")

        print("Nhập thông tin mới (Nếu không muốn đổi, nhấn Enter để bỏ qua):")
        while True:
            phone = input(" - Số điện thoại mới: ")
            
            # TRƯỜNG HỢP 1: Người dùng Enter để bỏ qua (Hợp lệ)
            if not phone:  # (phone là "" hoặc None)
                break 
            
            # TRƯỜNG HỢP 2: Người dùng nhập SĐT
            # Kiểm tra 1: Phải là số. Kiểm tra 2: Phải đủ 10 ký tự
            if phone.isdigit() and len(phone) == 10:
                break # Hợp lệ
            else:
                # Nếu 1 trong 2 điều kiện trên sai -> Báo lỗi
                print("Lỗi: SĐT phải là 10 chữ số. Vui lòng nhập lại (hoặc Enter để bỏ qua).")
        
        address = input(" - Địa chỉ mới: ")
        password = input(" - Mật khẩu mới: ")
        
        # Gọi hàm use_case
        update_user_info(
            user_id_to_update=user_id_to_update,
            updater_admin_level=updater_admin_level,
            phone=phone,
            address=address,
            password=password
        )
    except Exception as e:
        print(f"Lỗi khi cập nhật: {e}")
def menu_delete_user(deleter_admin_level): # <-- NHẬN LEVEL CỦA BẠN
    """Hàm này gọi chức năng Xóa (có kiểm tra level)"""
    print("\n--- [3] XÓA TÀI KHOẢN NGƯỜI DÙNG ---")
    try:
        #Lấy ID của người xóa
        user_id_to_delete = ""
        while not user_id_to_delete:
            user_id_to_delete = input("Nhập user_ID của người dùng bạn muốn XÓA: ")
        
        confirm = input(f"Bạn có CHẮC CHẮN muốn xóa user '{user_id_to_delete}' không? (gõ 'yes' để xác nhận): ")
        
        if confirm.lower() == 'yes':
            #  Gọi hàm use_case, chuyền id mục tiêu và lv của bản thân
            delete_user(
                user_id_to_delete=user_id_to_delete,
                deleter_admin_level=deleter_admin_level
            )
        else:
            print("Đã hủy thao tác xóa.")
    except Exception as e:
        print(f"Lỗi khi xóa: {e}")

def menu_create_announcement(admin_creator_id):
    """Hàm này là 'nút bấm' cho lựa chọn 4."""
    print("\n--- [4] TẠO THÔNG BÁO MỚI ---")
    
    # Lấy Scope (Hỏi riêng/chung)
    scope = None
    scope_map = {"1": "all", "2": "lecturer", "3": "student"}
    while scope is None:
        print("Vui lòng chọn phạm vi thông báo:")
        print("  1. Gửi cho tất cả (all)")
        print("  2. Gửi cho Giảng viên (lecturer)")
        print("  3. Gửi cho Sinh viên (student)")
        print("  (hoặc gõ 'q' để hủy)")
        
        scope_choice = input("Lựa chọn của bạn (1-3, q): ")
        if scope_choice.lower() == 'q':
            print("Đã hủy tạo thông báo.")
            return
        
        scope = scope_map.get(scope_choice)
        if scope is None:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
            
    # Lấy Content (Nội dung)
    content = ""
    while not content:
        content = input("Nhập nội dung thông báo: ")
        if not content:
            print("Nội dung không được để trống!")
    
    # Gọi Use Case
    try:
        print(f"\nĐang tạo thông báo (Scope: {scope}, Admin: {admin_creator_id})...")
        create_new_announcement(
            content=content,
            creator_id=admin_creator_id, # Lấy từ lúc đăng nhập
            scope=scope
        )
    except Exception as e:
        print(f"Lỗi khi tạo thông báo: {e}")

def menu_show_announcements():
    """Hàm này là 'nút bấm' cho lựa chọn 5."""
    print("\n--- [5] XEM TẤT CẢ THÔNG BÁO ---")
    try:
        show_all_announcements()
    except Exception as e:
        print(f"Lỗi khi xem thông báo: {e}")

def menu_update_announcement():
    """Hàm này là 'nút bấm' cho lựa chọn 6 (Cập nhật)"""
    print("\n--- [6] CẬP NHẬT THÔNG BÁO ---")
    print("(Mẹo: Chạy chức năng '5. Xem tất cả thông báo' để lấy ID)")
    
    try:
        notif_id = input("Nhập ID thông báo bạn muốn cập nhật: ")
        if not notif_id:
            print("Đã hủy. ID không được để trống.")
            return

        new_content = input("Nhập NỘI DUNG MỚI (bỏ trống nếu không muốn đổi): ")
        
        if not new_content:
            print("Không có gì để cập nhật. Đã hủy.")
            return
        
        update_announcement(notif_id, new_content)

    except Exception as e:
        print(f"Lỗi khi cập nhật thông báo: {e}")

def menu_delete_announcement():
    """Hàm này là 'nút bấm' cho lựa chọn 7 (Xóa)"""
    print("\n--- [7] XÓA THÔNG BÁO ---")
    print("(Mẹo: Chạy chức năng '5. Xem tất cả thông báo' để lấy ID)")
    
    try:
        notif_id = input("Nhập ID thông báo bạn muốn XÓA: ")
        if not notif_id:
            print("Đã hủy. ID không được để trống.")
            return

        confirm = input(f"Bạn có CHẮC CHẮN muốn xóa thông báo ID '{notif_id}' không? (gõ 'yes' để xác nhận): ")
        
        if confirm.lower() == 'yes':
            delete_announcement(notif_id)
        else:
            print("Đã hủy thao tác xóa.")
            
    except Exception as e:
        print(f"Lỗi khi xóa thông báo: {e}")

def run_admin_menu(admin_session):
    """
    admin_session = {"admin_id": "A001", "user_id": "U001", "level": 3}
    """
    # Lấy thông tin từ session
    current_admin_id = admin_session['admin_id']
    current_admin_level = admin_session['admin_level']
    
    while True:
        print("\n======================================")
        print(f"   ADMIN MENU (ID: {current_admin_id} | Level: {current_admin_level})") # <-- Hiển thị cả level
        print("======================================")
        print("--- Quản lý người dùng ---")
        print("1. Hiển thị danh sách người dùng")
        print("2. Chỉnh sửa thông tin người dùng")
        print("3. Xóa tài khoản người dùng")
        print("--- Quản lý thông báo ---")
        print("4. Tạo thông báo mới")
        print("5. Xem tất cả thông báo (ĐỂ LẤY ID)")
        print("6. Cập nhật thông báo (THEO ID)")
        print("7. Xóa thông báo (THEO ID)")
        print("-------------------------")
        print("8. Quay lại (Đăng xuất)")
        print("--------------------------------------")
        
        choice = input("Vui lòng chọn chức năng (1-8): ")
        
        if choice == '1':
            menu_show_users()
        elif choice == '2':
            menu_update_user(current_admin_level) # Chuyền level 
        elif choice == '3':
            menu_delete_user(current_admin_level) # Chuyền level 
        elif choice == '4':
            menu_create_announcement(current_admin_id) # Chuyền ID admin
        elif choice == '5':
            menu_show_announcements()
        elif choice == '6':
            menu_update_announcement() 
        elif choice == '7':
            menu_delete_announcement() 
        elif choice == '8':
            print("Đang đăng xuất...")
            break 
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
        
        input("\nNhấn Enter để quay lại menu admin...")

# KHỐI CHẠY TEST
if __name__ == "__main__":
    print(">>> CHẠY TEST RIÊNG FILE ADMIN_MENU <<<")
    
    test_session = {
        "admin_id": "A_Test_ID", 
        "user_id": "U_Test_ID", 
        "admin_level": 3 
    }
    
    # Chạy menu với session giả lập
>>>>>>> 0015678bc892863b15e8434d9f3b97cd7324b7dd
    run_admin_menu(test_session)