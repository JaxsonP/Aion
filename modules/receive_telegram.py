import os
import time

from multiprocessing import Process
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

aion_pipe = None
bot_token = os.environ['AION_BOT_TOKEN']
chat_id = os.environ['TELEGRAM_CHAT_ID']
updater = None

"""def receive_telegram():
    data = request.get_data().decode()
    print(data)"""

def start_listener(port, _aion_pipe):
    global aion_pipe
    aion_pipe = _aion_pipe

    updater = Updater(bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("shutdown", shutdown))
    dispatcher.add_handler(MessageHandler(Filters.all, receive_message))
    dispatcher.add_error_handler(error, True)

    updater.start_webhook(port=port)
    
    """global aion_pipe
    aion_pipe = _aion_pipe
    print("test1")
    server = Process(target=app.run(port=port, debug=False, use_reloader=False))
    #server.start()
    print('Flask server terminated')"""

def receive_message(update, context):
    print("Received message: ", update)

def error(update, context):
    print("Received Error: ", update)

def shutdown(update, context):
    print("Received shutdown command")
    pass

def set_webhook_url (url):
    #changing the webhook url
    print("Setting webhook url")
    #os.system(f'twilio phone-numbers:update {phone_number} --sms-url {url}/atlas')
    return