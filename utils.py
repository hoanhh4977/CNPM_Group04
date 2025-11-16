<<<<<<< HEAD
import random

def generate_attendance_code():
    return str(random.randint(10000, 99999))
=======
import random
import string

def generate_attendance_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
>>>>>>> 0015678bc892863b15e8434d9f3b97cd7324b7dd
