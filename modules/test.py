
import modules.telegram_interface

user_functions = ['echo']

def echo (text):
    modules.telegram_interface.send_message(text)