import sys
sys.stdout.reconfigure(encoding='utf-8')

from src.service.student_service import StudentService
from src.service.lecturer_service import LecturerService
from src.service.session_service import SessionService

print("🎓 HỆ THỐNG ĐIỂM DANH SINH VIÊN")

role = input("Bạn là ai? (Student/Lecturer): ").strip()
user_id = input("Nhập ID người dùng: ").strip()

if role == "Student":
    student_service = StudentService()
    session_service = SessionService()

    print("\n1. Xem lịch học\n2. Điểm danh\n3. Xem kết quả điểm danh")
    choice = input("Chọn chức năng: ").strip()

    if choice == "1":
        sessions = session_service.get_upcoming_sessions()
        print(f"\n📘 Lịch học của sinh viên {user_id}:")
        for s in sessions:
            print(f"- Ngày: {s['session_date']} | Ca: {s['time_slot']} | Môn: {s['subject_name']} | Mã buổi học: {s['session_id']}")
    elif choice == "2":
        session_id = input("🔢 Nhập mã buổi học: ").strip()
        code_input = input("🔐 Nhập mã điểm danh: ").strip()
        result = student_service.mark_attendance(user_id, session_id, code_input)
        print(result)
    elif choice == "3":
        results = student_service.view_attendance_results(user_id)
        print(f"\n📋 Kết quả điểm danh của {user_id}:")
        for r in results:
            print(f"Buổi học: {r['session_id']} | Thời gian: {r['check_in_time']} | Trạng thái: {r['status']}")
    else:
        print("❌ Chức năng không hợp lệ.")

elif role == "Lecturer":
    lecturer_service = LecturerService()

    print("\n1. Tạo buổi học\n2. Xem điểm danh lớp\n3. Sửa kết quả điểm danh")
    choice = input("Chọn chức năng: ").strip()

    if choice == "1":
        subject_name = input("📘 Tên môn học: ").strip()
        time_slot = input("🕒 Ca học: ").strip()
        code = lecturer_service.create_session(user_id, subject_name, time_slot)
        print(f"✅ Buổi học đã tạo. Mã điểm danh: {code}")
    elif choice == "2":
        session_id = input("🔢 Nhập mã buổi học: ").strip()
        results = lecturer_service.view_class_attendance(session_id)
        print(f"\n📊 Kết quả điểm danh buổi học {session_id}:")
        for r in results:
            print(f"Sinh viên: {r['student_id']} | Thời gian: {r['check_in_time']} | Trạng thái: {r['status']}")
    elif choice == "3":
        att_id = input("🔄 Nhập mã điểm danh: ").strip()
        new_status = input("📝 Trạng thái mới (Present/Absent/Late/Excused): ").strip()
        result = lecturer_service.edit_attendance(att_id, new_status)
        print(result)
    else:
        print("❌ Chức năng không hợp lệ.")


else:
    print("❌ Vai trò không hợp lệ.")
