from src.service.student_service import StudentService
from src.service.lecturer_service import LecturerService
from src.service.session_service import SessionService
from src.service.attendance_service import AttendanceService

student_service = StudentService()
lecturer_service = LecturerService()
session_service = SessionService()
attendance_service = AttendanceService()

def run_console():
    while True:
        print("\n MENU CHÍNH")
        print("1. Giảng viên")
        print("2. Sinh viên")
        print("0. Thoát")
        role = input(" Chọn vai trò: ")
        if role == "1":
            run_lecturer_menu()
        elif role == "2":
            run_student_menu()
        elif role == "0":
            break

def run_lecturer_menu():
    while True:
        print("\n MENU GIẢNG VIÊN")
        print("1. Tạo buổi học")
        print("2. Xem điểm danh")
        print("3. Cập nhật trạng thái")
        print("0. Quay lại")
        choice = input(" Chọn chức năng: ")
        if choice == "1":
            create_session()
        elif choice == "2":
            view_attendance()
        elif choice == "3":
            update_status()
        elif choice == "0":
            break

def run_student_menu():
    while True:
        print("\n MENU SINH VIÊN")
        print("1. Điểm danh")
        print("2. Xem lịch học")
        print("0. Quay lại")
        choice = input(" Chọn chức năng: ")
        if choice == "1":
            mark_attendance()
        elif choice == "2":
            view_schedule()
        elif choice == "0":
            break

def create_session():
    print(" TẠO BUỔI HỌC MỚI")
    subject_name = input("Tên môn học: ")
    time_slot = input("Ca học (Sáng / Chiều): ")

    session = lecturer_service.create_session(
        subject_name=subject_name,
        time_slot=time_slot
    )

    print("\n Buổi học đã được tạo thành công!")
    print(f" Môn học: {session['subject_name']}")
    print(f" Ca học: {session['time_slot']}")
    print(f" Ngày học: {session['session_date']}")
    print(f" Mã buổi học: {session['session_id']}")
    print(f" Mã giảng viên: {session['lecturer_id']}")
    print(f" Mã điểm danh: {session['attendance_code']}")

def view_attendance():
    session_id = input("Mã buổi học: ")
    data = lecturer_service.view_attendance_by_session(session_id)

    if not data:
        print("❌ Không có dữ liệu điểm danh.")
        return

    print("\n DANH SÁCH ĐIỂM DANH:")
    for record in data:
        print(f"- Sinh viên: {record['student_id']} | Trạng thái: {record['status']}")

def update_status():
    student_id = input("Mã sinh viên: ")
    session_id = input("Mã buổi học: ")
    new_status = input("Trạng thái mới (present/absent/late): ")
    result = lecturer_service.update_attendance_status_by_student(student_id, session_id, new_status)
    print(result)


def mark_attendance():
    student_id = input("Mã sinh viên: ")
    session_id = input("Mã buổi học: ")
    code = input("Mã điểm danh: ")
    result = student_service.mark_attendance(student_id, session_id, code)
    print(" Kết quả:", result)

def view_schedule():
    student_id = input(" Mã sinh viên: ")
    sessions = session_service.get_sessions_for_student(student_id)

    if not sessions:
        print(" Không tìm thấy lịch học nào.")
        return

    print("\n LỊCH HỌC CỦA SINH VIÊN:")
    for s in sessions:
        print(f"- {s['session_date']} | {s['time_slot']} | {s['subject_name']} | Mã buổi: {s['session_id']}")
