from src.storage.repositories.user_repository import UserRepository
def show_all_users():
    repo = UserRepository()
    users = repo.get_all_users() # Giả sử hàm này trả về một danh sách (list)
    print("=== DANH SÁCH NGƯỜI DÙNG ===")
    # Kiểm tra xem có user nào không
    if not users:
        print("Không tìm thấy người dùng nào.")
        return
    # In ra danh sách
    for u in users:
        print(f"ID: {u.get('user_id')}, Tên: {u.get('full_name')}, Loại: {u.get('account_type')}, SĐT: {u.get('phone_number')}")
        # print(u) # Hoặc có thể in ra toàn bộ object để xem
# Khối test       
if __name__ == "__main__":
    show_all_users()