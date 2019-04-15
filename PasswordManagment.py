class PasswordManagment:

    def __init__(self, file_path):
        self.file_path = file_path

	#Gets the next password to crack from the file, critical for the threads to be synchronized.
    def get_next_password_from_file(self):
        password_file = open(self.file_path)
        for password in password_file:
            if not password.strip():
                continue
            return (password)

    #Loads the password into the RAM.
    def load_passwords_into_ram(self):
        self.password_file = open(self.file_path).readlines()

	#Gets the next password to crack from the memory, critical for the threads to be synchronized.
    def get_next_password_from_ram(self):
        for password in self.password_file:
            if not password.strip():
                continue
            return (password)