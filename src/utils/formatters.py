"""
Formatters - Định dạng hiển thị cho console
"""

def print_header(title: str):
    """In tiêu đề lớn"""
    print("\n" + "=" * 60)
    print(f"  {title.center(56)}")
    print("=" * 60)

def print_section(title: str):
    """In tiêu đề phần"""
    print("\n" + "-" * 60)
    print(f"  {title}")
    print("-" * 60)

def print_table(headers: list, rows: list):
    """
    In bảng dữ liệu
    headers: Danh sách tiêu đề cột
    rows: Danh sách các dòng (mỗi dòng là list)
    """
    if not rows:
        print("  (Không có dữ liệu)")
        return

    # Tính độ rộng cột
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    # In header
    header_line = "  " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    print(header_line)
    print("  " + "-" * (len(header_line) - 2))

    # In rows
    for row in rows:
        row_line = "  " + " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
        print(row_line)

def print_success(message: str):
    """In thông báo thành công"""
    print(f"\n✅ {message}")

def print_error(message: str):
    """In thông báo lỗi"""
    print(f"\n❌ {message}")

def print_info(message: str):
    """In thông báo thông tin"""
    print(f"\nℹ️  {message}")

def print_warning(message: str):
    """In cảnh báo"""
    print(f"\n⚠️  {message}")

def print_menu(title: str, options: list, show_back: bool = True):
    """
    In menu với các lựa chọn
    options: List of tuples (key, description)
    """
    print_header(title)
    for key, desc in options:
        print(f"  {key}. {desc}")
    if show_back:
        print(f"  0. Quay lại")
    print("-" * 60)

def format_datetime(dt_string: str) -> str:
    """
    Định dạng datetime string
    Input: ISO format
    Output: DD/MM/YYYY HH:MM:SS
    """
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        return dt.strftime("%d/%m/%Y %H:%M:%S")
    except:
        return dt_string

def format_date(date_string: str) -> str:
    """
    Định dạng date string
    Input: YYYY-MM-DD
    Output: DD/MM/YYYY
    """
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(date_string)
        return dt.strftime("%d/%m/%Y")
    except:
        return date_string

def wait_for_enter(message: str = "Nhấn Enter để tiếp tục..."):
    """Chờ người dùng nhấn Enter"""
    input(f"\n{message}")
