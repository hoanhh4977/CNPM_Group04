from src.service.student_service import StudentService
from src.service.lecturer_service import LecturerService
from src.service.session_service import SessionService

from src.repository.lecturer_repository import LecturerRepository
from src.repository.student_repository import StudentRepository

from src.service.main_console import run_console  # Đảm bảo file này có hàm run_console()

def run_tests():
    print("✅ Bắt đầu kiểm thử...")

    # Tạo dữ liệu mặc định
    LecturerRepository().insert_default_lecturer()
    StudentRepository().insert_default_student()

    student_service = StudentService()
    lecturer_service = LecturerService()
    session_service = SessionService()

    lecturer_id = "U001"
    student_id = "U002"

    # ✅ Tạo buổi học với đầy đủ tham số
    session_id = "1"
    attendance_code = "ABC123"
    subject_name = "Toán"
    time_slot = "Sáng"

    session = session_service.create_session(
        session_id,
        lecturer_id,
        attendance_code,
        subject_name,
        time_slot
    )
    print(f"✅ Buổi học: {session_id} | Mã điểm danh: {attendance_code}")

    # ✅ Sinh viên điểm danh
    result = student_service.mark_attendance(student_id, session_id, attendance_code)
    print(f"✅ Điểm danh: {result}")

    # ✅ Giảng viên xem điểm danh
    data = lecturer_service.view_attendance_by_session(session_id)
    print(f"✅ Dữ liệu điểm danh: {data}")

    # ✅ Giảng viên sửa trạng thái
    if data and len(data) > 0:
        attendance_id = data[0]["attendance_id"]
        result = lecturer_service.update_attendance_status(attendance_id, "Late")
        print(f"✅ Sửa trạng thái: {result}")
    else:
        print("❌ Không có dữ liệu điểm danh để sửa.")

    print("✅ Kiểm thử hoàn tất.")

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
