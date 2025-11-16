import pandas as pd
def test_connection():
    print("File test_connection.py đang chạy!")
    from storage.client import get_supabase
    supabase = get_supabase()
    print("Kết nối Supabase thành công!")
    try:
        response = supabase.table("User").select("*").execute()
        data = response.data  # Lấy dữ liệu từ response
        if data:
            print("Kết quả trả về từ Supabase:\n")
            df = pd.DataFrame(data)
            print(df.to_string(index=False))  # In bảng đẹp, không index
        else:
            print("Không có dữ liệu trong bảng User.")
    except Exception as e:
        print("Lỗi xảy ra:", e)

if __name__ == "__main__":
    test_connection()