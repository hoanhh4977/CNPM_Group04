from supabase import create_client

def get_supabase():    
    client = create_client(
        supabase_url="https://aedesxngtubaapvileww.supabase.co",
        supabase_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFlZGVzeG5ndHViYWFwdmlsZXd3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mjg2MDk1OCwiZXhwIjoyMDc4NDM2OTU4fQ.0uHtoQfyAZjmXBnUP6F_nHt2StIv_e_csL8TA5NWabo"
    )
    return client

