from supabase_client import supabase

class StudentRepository:
    def get_students_by_class(self, class_name):
        return supabase.table("student").select("*").eq("class", class_name).execute()

    def get_student_by_id(self, student_id):
        return supabase.table("student").select("*").eq("student_id", student_id).execute()