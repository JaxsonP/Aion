
import modules.telegram_interface

user_functions = ['echo']

def echo (text):
    modules.telegram_interface.send_message(text)
    return True

def concat (text1, text2):
    modules.telegram_interface.send_message(text1 + text2)
    return True