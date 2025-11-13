from supabase_client import supabase
from datetime import datetime

def get_students_by_class(class_name):
    result = supabase.table("student").select("*").eq("class_name", class_name).execute()
    return result.data

def test_get_students_by_class(supabase_client):
    result = get_students_by_class("CTK42")
    assert isinstance(result, list)
    for student in result:
        assert student["class"] == "CTK42"

def mark_attendance(student_id):
    session_id = input("🔢 Nhập mã buổi học: ")
    code_input = input("🔐 Nhập mã điểm danh: ")

    session = supabase.table("session").select("*").eq("session_id", session_id).eq("attendance_code", code_input).execute()
    if session.data:
        supabase.table("attendance").insert({
            "attendance_id": str(int(datetime.now().timestamp())),
            "student_id": student_id,
            "session_id": session_id,
            "check_in_time": datetime.now().isoformat(),
            "status": "Present"
        }).execute()
        print("✅ Điểm danh thành công!")
    else:
        print("❌ Mã điểm danh không hợp lệ.")

def view_attendance_results(student_id):
    results = supabase.table("attendance").select("*").eq("student_id", student_id).execute()
    print(f"\n📋 Kết quả điểm danh của {student_id}:")
    for r in results.data:
        print(f"Buổi học: {r['session_id']} | Thời gian: {r['check_in_time']} | Trạng thái: {r['status']}")