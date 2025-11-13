from supabase_client import supabase
from datetime import date, datetime
from utils import generate_attendance_code
def get_lecturer_by_id(lecturer_id):
    result = supabase.table("lecturer").select("*").eq("lecturer_id", lecturer_id).execute()
    return result.data

def create_session(lecturer_id):
    subject_name = input("📘 Tên môn học: ")
    time_slot = input("🕒 Ca học: ")
    session_id = str(hash(subject_name + time_slot + lecturer_id) % 100000)
    attendance_code = generate_attendance_code()

    supabase.table("session").insert({
        "session_id": session_id,
        "lecturer_id": lecturer_id,
        "session_date": date.today().isoformat(),
        "time_slot": time_slot,
        "subject_name": subject_name,
        "attendance_code": attendance_code
    }).execute()
    print(f"✅ Buổi học đã tạo. Mã điểm danh: {attendance_code}")

def view_class_attendance(session_id):
    results = supabase.table("attendance").select("*").eq("session_id", session_id).execute()
    print(f"\n📊 Kết quả điểm danh buổi học {session_id}:")
    for r in results.data:
        print(f"Sinh viên: {r['student_id']} | Thời gian: {r['check_in_time']} | Trạng thái: {r['status']}")

def edit_attendance(attendance_id, new_status):
    supabase.table("attendance").update({"status": new_status}).eq("attendance_id", attendance_id).execute()
    print("✅ Đã cập nhật trạng thái điểm danh.")