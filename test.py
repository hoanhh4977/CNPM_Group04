from src.services.auth_service import AuthService

auth_service = AuthService()

#. Vietnamese prompts for console login/register
def test_login():
    auth_service = AuthService()
    auth_service.console_login()

def test_register():
    auth_service = AuthService()
    auth_service.console_register()
    
if __name__ == "__main__":
    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            test_login()
        elif choice == "2":
            test_register()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")