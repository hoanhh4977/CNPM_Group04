from src.service.student_service import StudentService
from src.service.lecturer_service import LecturerService
from src.service.session_service import SessionService
from src.service.attendance_service import AttendanceService

student_service = StudentService()
lecturer_service = LecturerService()
session_service = SessionService()
attendance_service = AttendanceService()

#  Sinh viên điểm danh
def mark_attendance():
    student_id = input("Mã sinh viên: ")
    session_id = input("Mã buổi học: ")
    code = input("Mã điểm danh: ")
    result = student_service.mark_attendance(student_id, session_id, code)
    print(" Kết quả:", result)

#  Tạo buổi học
def create_session():
    session_id = input("Mã buổi học: ")
    lecturer_id = input("Mã giảng viên: ")
    code = input("Mã điểm danh: ")
    result = session_service.create_session({
        "session_id": session_id,
        "lecturer_id": lecturer_id,
        "attendance_code": code
    })
    print(" Kết quả:", result)

#  Xem điểm danh
def view_attendance_by_session():
    session_id = input("Mã buổi học: ")
    data = lecturer_service.view_attendance_by_session(session_id)
    if not data:
        print(" Không có dữ liệu.")
        return
    for i, record in enumerate(data, 1):
        print(f"{i}. Mã SV: {record['student_id']} - Trạng thái: {record['status']} - ID: {record['attendance_id']}")

#  Cập nhật trạng thái
def update_attendance_status():
    attendance_id = input("Mã điểm danh: ")
    status = input("Trạng thái mới (Present / Late / Absent): ")
    result = lecturer_service.update_attendance_status(attendance_id, status)
    print(" Kết quả:", result)

#  Xóa điểm danh
def delete_attendance():
    attendance_id = input("Mã điểm danh cần xóa: ")
    result = attendance_service.delete(attendance_id)
    print(" Kết quả xóa:", result)

#  Menu chính
def run_console():
    while True:
        print("\n === MENU ĐIỂM DANH ===")
        print("1. Tạo buổi học")
        print("2. Sinh viên điểm danh")
        print("3. Xem danh sách điểm danh")
        print("4. Cập nhật trạng thái điểm danh")
        print("5. Xóa điểm danh")
        print("0. Thoát")

        choice = input(" Chọn chức năng: ")
        if choice == "1":
            create_session()
        elif choice == "2":
            mark_attendance()
        elif choice == "3":
            view_attendance_by_session()
        elif choice == "4":
            update_attendance_status()
        elif choice == "5":
            delete_attendance()
        elif choice == "0":
            print(" Kết thúc chương trình.")
            break
        else:
            print(" Lựa chọn không hợp lệ.")
