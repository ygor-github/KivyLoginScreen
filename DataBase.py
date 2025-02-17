import datetime
import bcrypt

class DataBase:
    def __init__(self, filename):
        self.filename = filename
        self.users = None
        self.file = None
        self.load()
    
    def load(self):
        try:
            with (open(self.filename, 'r') as file):
                for line in file:
                    email, password, name, created = line.strip().split(';')
                    self.users[email] = (password, name, created)
        except FileNotFoundError:
            print('File not found. It is created a new to save data')
        except Exception as e:
            print(f'Error to load data: {e}')
        self.file.close()
    
    def get_user(self, email):
        return self.users.get(email, -1)
    
    def add_user(self, email, password, name):
        if email.strip() not in self.users:
            hashed_password = bcrypt.hashpw(password.strip().encode(), bcrypt.gensalt()).decode()
            self.users[email.strip()] = (
                hashed_password.strip(),
                name.strp(),
                DataBase.get_date()
            )
            self.save()
            return 1
        else:
            print('Email exist already')
            return -1
    
    def validate(self, email, password):
        if self.get_user(email) != -1:
            return bcrypt.checkpw(password.econde(), self.users[email][0].encode())
        else:
            return False
    
    def save(self):
        try:
            with open(self.filename, 'w') as file:
                for email, data in self.users.items():
                    file.write(f'{email};{data[0]};{data[1]};{data[2]}\n')
        except Exception as e:
            print(f'Error to save data: {e}')
    
    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(' ')[0]