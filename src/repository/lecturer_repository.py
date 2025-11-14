from supabase_client import supabase

class LecturerRepository:
    def get_lecturer_by_id(self, lecturer_id):
        return supabase.table("lecturer").select("*").eq("lecturer_id", lecturer_id).execute()

    def get_all_lecturers(self):
        return supabase.table("lecturer").select("*").execute()