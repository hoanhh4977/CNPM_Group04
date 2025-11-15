from src.service.student_service import StudentService
from src.service.lecturer_service import LecturerService
from src.service.session_service import SessionService
from src.service.attendance_service import AttendanceService
from src.service.main_console import run_console

def run_tests():
    print("\n BẮT ĐẦU KIỂM THỬ TỰ ĐỘNG")

    # Mã giả định
    lecturer_id = "L001"
    student_id = "S001"
    subject = "Python nâng cao"
    time_slot = "Sáng"

    # Khởi tạo service
    student_service = StudentService()
    lecturer_service = LecturerService()

    #  Tự động tạo giảng viên và sinh viên nếu chưa có
    lecturer_service.ensure_lecturer_exists(lecturer_id)
    student_service.ensure_student_exists(student_id)

    #  Tạo buổi học
    session = lecturer_service.create_session(lecturer_id, subject, time_slot)
    session_id = session["session_id"]
    attendance_code = session["attendance_code"]
    print(f"\n Buổi học đã tạo: {session}")

    #  Sinh viên điểm danh
    result = student_service.mark_attendance(student_id, session_id, attendance_code)
    print(f"\n Kết quả điểm danh: {result}")

    #  Xem danh sách điểm danh
    attendance_list = lecturer_service.view_attendance_by_session(session_id)
    print(f"\n📋 Danh sách điểm danh:")
    for record in attendance_list:
        print(record)

if __name__ == "__main__":
    print("1. Kiểm thử tự động")
    print("2. Chạy thủ công")
    mode = input(" Chọn chế độ: ")
    if mode == "1":
        run_tests()
    else:
        run_console()
