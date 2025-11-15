from src.service.student_service import StudentService
from src.service.lecturer_service import LecturerService
from src.service.session_service import SessionService

from src.repository.lecturer_repository import LecturerRepository
from src.repository.student_repository import StudentRepository

def run_tests():
    print("✅ Bắt đầu kiểm thử...")

    # 🔧 Tạo dữ liệu mặc định nếu chưa có
    LecturerRepository().insert_default_lecturer()
    StudentRepository().insert_default_student()

    # 🔧 Khởi tạo các service
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
    print(f" Buổi học: {session_id} | Mã điểm danh: {attendance_code}")

    # 2. Sinh viên điểm danh
    result = student_service.mark_attendance(student_id, session_id, attendance_code)
    print(f" Điểm danh: {result}")

    # 3. Giảng viên xem điểm danh
    data = lecturer_service.view_attendance_by_session(session_id)
    print(f" Dữ liệu điểm danh: {data}")

    # 4. Giảng viên sửa trạng thái nếu có dữ liệu
    if data and len(data) > 0:
        attendance_id = data[0]["attendance_id"]
        result = lecturer_service.update_attendance_status(attendance_id, "Late")
        print(f" Sửa trạng thái: {result}")
    else:
        print(" Không có dữ liệu điểm danh để sửa.")

    print(" Kiểm thử hoàn tất.")

if __name__ == "__main__":
    run_tests()
