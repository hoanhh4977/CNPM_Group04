from supabase import create_client

url = "https://aedesxngtubaapvileww.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFlZGVzeG5ndHViYWFwdmlsZXd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI4NjA5NTgsImV4cCI6MjA3ODQzNjk1OH0.50HsLqMecvlmnbNWRJZXKr3BBhi31s286L4QZSNKEHQ"

supabase = create_client(url, key)