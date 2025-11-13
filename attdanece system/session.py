from supabase_client import supabase
from datetime import date

def get_session_for_lecturer(supabase, lecturer_id):
    result = supabase.table("session").select("*").eq("lecturer_id", lecturer_id).execute()
    return result.data

def view_session(student_id):
    today = date.today().isoformat()
    sessions = supabase.table("session").select("*").gte("session_date", today).execute()
    print(f"\n📘 Lịch học của sinh viên {student_id}:")
    if not sessions.data:
        print("❌ Không có buổi học nào.")
    for s in sessions.data:
        print(f"- Ngày: {s['session_date']} | Ca: {s['time_slot']} | Môn: {s['subject_name']} | Mã buổi học: {s['session_id']}")
