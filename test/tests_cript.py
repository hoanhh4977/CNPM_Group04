from src.service.student_service import StudentService
from src.service.lecturer_service import LecturerService
from src.service.session_service import SessionService
from src.service.attendance_service import AttendanceService

def run_tests():
    print("✅ Bắt đầu kiểm thử...")

    student_service = StudentService()
    lecturer_service = LecturerService()
    session_service = SessionService()
    attendance_service = AttendanceService()

    # 1. Tạo giảng viên
    lecturer = lecturer_service.create_lecturer("U001")
    lecturer_id = lecturer[0]["lecturer_id"]
    print(f" Giảng viên: {lecturer_id}")

    # 2. Tạo sinh viên
    student = student_service.create_student("U002", "K23CNTT")
    student_id = student[0]["student_id"]
    print(f" Sinh viên: {student_id}")

    # 3. Tạo buổi học
    session = session_service.create_session(lecturer_id, "Toán", "Sáng")
    session_id = session[0]["session_id"]
    attendance_code = session[0]["attendance_code"]
    print(f" Buổi học: {session_id} | Mã điểm danh: {attendance_code}")

    # 4. Sinh viên điểm danh
    result = student_service.mark_attendance(student_id, session_id, attendance_code)
    print(f" Điểm danh: {result}")

    # 5. Giảng viên xem điểm danh
    data = lecturer_service.view_attendance_by_session(session_id)
    print(f" Dữ liệu điểm danh: {data}")

    # 6. Giảng viên sửa trạng thái nếu có dữ liệu
    if data and len(data) > 0:
        attendance_id = data[0]["attendance_id"]
        result = lecturer_service.update_attendance_status(attendance_id, "Late")
        print(f" Sửa trạng thái: {result}")
    else:
        print(" Không có dữ liệu điểm danh để sửa.")

    print(" Kiểm thử hoàn tất.")

if __name__ == "__main__":
    run_tests()
