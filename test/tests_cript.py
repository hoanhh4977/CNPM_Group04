from src.service.student_service import StudentService
from src.service.lecturer_service import LecturerService
from src.service.session_service import SessionService
<<<<<<< HEAD

from src.repository.lecturer_repository import LecturerRepository
from src.repository.student_repository import StudentRepository

from src.service.main_console import run_console

def run_tests():
    print("✅ Bắt đầu kiểm thử...")

    # ✅ Tạo dữ liệu mặc định nếu chưa có
    LecturerRepository().insert_default_lecturer()
    StudentRepository().insert_default_student()

    # ✅ Khởi tạo các service
    student_service = StudentService()
    lecturer_service = LecturerService()
    session_service = SessionService()

    # ✅ Dùng ID mặc định
    lecturer_id = "U001"
    student_id = "U002"

    # 1. Tạo buổi học
    session = session_service.create_session(lecturer_id, "Toán", "Sáng")
    session_id = session[0]["session_id"]
    attendance_code = session[0]["attendance_code"]
    print(f"✅ Buổi học: {session_id} | Mã điểm danh: {attendance_code}")

    # 2. Sinh viên điểm danh
    result = student_service.mark_attendance(student_id, session_id, attendance_code)
    print(f"✅ Điểm danh: {result}")

    # 3. Giảng viên xem điểm danh
    data = lecturer_service.view_attendance_by_session(session_id)
    print(f"✅ Dữ liệu điểm danh: {data}")

    # 4. Giảng viên sửa trạng thái nếu có dữ liệu
    if data and len(data) > 0:
        attendance_id = data[0]["attendance_id"]
        result = lecturer_service.update_attendance_status(attendance_id, "Late")
        print(f"✅ Sửa trạng thái: {result}")
    else:
        print("❌ Không có dữ liệu điểm danh để sửa.")

    print("✅ Kiểm thử hoàn tất.")

# ✅ Menu chọn chế độ
if __name__ == "__main__":
    print("🎓 === CHỌN CHẾ ĐỘ KIỂM THỬ ===")
    print("1. Kiểm thử tự động")
    print("2. Kiểm thử thủ công qua console")
    mode = input("👉 Nhập lựa chọn (1 hoặc 2): ")

    if mode == "1":
        run_tests()
    elif mode == "2":
        run_console()
    else:
        print("⚠️ Lựa chọn không hợp lệ.")
=======
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
    print(f"\n Danh sách điểm danh:")
    for record in attendance_list:
        print(record)

if __name__ == "__main__":
    print(" Đang chạy ở chế độ thủ công...")

    run_console()
>>>>>>> 0015678bc892863b15e8434d9f3b97cd7324b7dd
