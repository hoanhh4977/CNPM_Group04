from src.service.student_service import StudentService
from src.service.lecturer_service import LecturerService
from src.service.session_service import SessionService
from src.service.attendance_service import AttendanceService

def main():
    student_service = StudentService()
    lecturer_service = LecturerService()
    session_service = SessionService()
    attendance_service = AttendanceService()

    print("🎓 Hệ thống điểm danh")
    print("1. Tạo giảng viên")
    print("2. Tạo sinh viên")
    print("3. Tạo buổi học")
    print("4. Sinh viên điểm danh")
    print("5. Xem điểm danh theo buổi")
    print("6. Sửa trạng thái điểm danh")
    print("7. Thoát")

    while True:
        choice = input("👉 Chọn chức năng: ")
        if choice == "1":
            uid = input("Nhập user_id giảng viên: ")
            result = lecturer_service.create_lecturer(uid)
            print(f"✅ Tạo giảng viên: {result}")

        elif choice == "2":
            uid = input("Nhập user_id sinh viên: ")
            class_name = input("Nhập lớp: ")
            result = student_service.create_student(uid, class_name)
            print(f"✅ Tạo sinh viên: {result}")

        elif choice == "3":
            lid = input("Nhập lecturer_id: ")
            subject = input("Tên môn học: ")
            slot = input("Ca học (Sáng/Chiều): ")
            result = session_service.create_session(lid, subject, slot)
            print(f"✅ Tạo buổi học: {result}")

        elif choice == "4":
            sid = input("Nhập student_id: ")
            sess = input("Nhập session_id: ")
            code = input("Nhập mã điểm danh: ")
            result = student_service.mark_attendance(sid, sess, code)
            print(result)

        elif choice == "5":
            sess = input("Nhập session_id: ")
            data = lecturer_service.view_attendance_by_session(sess)
            for d in data:
                print(d)

        elif choice == "6":
            aid = input("Nhập attendance_id: ")
            status = input("Trạng thái mới: ")
            result = lecturer_service.update_attendance_status(aid, status)
            print(result)

        elif choice == "7":
            print("👋 Tạm biệt!")
            break

        else:
            print("❌ Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    main()
    
