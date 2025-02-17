from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from DataBase import DataBase
import bcrypt

class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    
    def submit(self):
        if self.namee.text != '' and '@' in self.email.text and '.' in self.email.text:
            if self.password.text !='':
                hashed_password = bcrypt.hashpw(self.password.text.encode('utf-8'), bcrypt.gensalt())
                db.add_user(self.email.text, hashed_password.decode('utf-8'), self.namee.text)
                self.reset()
                sm.current = 'login'
            else:
                invalid_form()
        else:
            invalid_form()
    
    def login(self):
        self.reset()
        sm.current = 'login'
    
    def reset(self):
        self.email.text = ''
        self.password.text = ''
        self.namee.text = ''

class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    
    def login_btn(self):
        stored_password = db.get_user(self.email.text)
        if stored_password and bcrypt.checkpw(self.password.text.encode('utf-8'), stored_password.encode('utf-8')):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = 'main'
        else:
            invalid_login()
    
    def create_btn(self):
        self.reset()
        sm.current = 'create'
    
    def reset(self):
        self.email.text = ''
        self.password.text = ''


class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ''
    
    def log_out(self):
        sm.current = 'login'
    
    def on_enter(self, *args):
        _, name, created = db.get_user(self.current)
        self.n.text = f'Account Name: {name}'
        self.email.text = f'Email: {self.current}'
        self.created.text = f'Created On: {created}'

class WindowManager(ScreenManager):
    pass

def invalid_login():
    pop = Popup(title = 'Invalid Login',
                contect = Label(text='Invalid username or password'),
                size_hint = (None, None), size = (400, 400))
    pop.open()

def invalid_form():
    pop = Popup(title = 'Invalid Form',
                content = Label( text ='Please fill in all inputs with valid information.'),
                size_hint = (None, None), sizze = (400, 400))
    pop.open()

kv = Builder.load_file('my.kv')
db = DataBase('users.text')

sm = WindowManager()
screens = [LoginWindow(name='login'), CreateAccountWindow(name='create'), MainWindow(name='main')]
for Screen in screens:
    sm.add_widget(Screen)

sm.current = 'login'

class MyMainApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    MyMainApp().run()






