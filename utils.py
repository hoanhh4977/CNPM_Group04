import random
import string

def generate_attendance_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
