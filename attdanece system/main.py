import sys
sys.stdout.reconfigure(encoding='utf-8')
from student import mark_attendance, view_attendance_results
from lecturer import create_session, view_class_attendance, edit_attendance
from session import view_session
print("HỆ THỐNG ĐIỂM DANH SINH VIÊN".encode('utf-8').decode('utf-8'))
role = input("Bạn là ai? (Student/Lecturer): ").strip()
user_id = input("Nhập ID người dùng: ").strip()

if role == "Student":
    print("\n1. Xem lịch học\n2. Điểm danh\n3. Xem kết quả điểm danh")
    choice = input("Chọn chức năng: ")
    if choice == "1":
        view_session(user_id)
    elif choice == "2":
        mark_attendance(user_id)
    elif choice == "3":
        view_attendance_results(user_id)

elif role == "Lecturer":
    print("\n1. Tạo buổi học\n2. Xem điểm danh lớp\n3. Sửa kết quả điểm danh")
    choice = input("Chọn chức năng: ")
    if choice == "1":
        create_session(user_id)
    elif choice == "2":
        session_id = input("Nhập mã buổi học: ")
        view_class_attendance(session_id)
    elif choice == "3":
        att_id = input("Nhập mã điểm danh: ")
        new_status = input("Trạng thái mới (Present/Absent/Late/Excused): ")
        edit_attendance(att_id, new_status)
else:
    print("❌ Vai trò không hợp lệ.")
    