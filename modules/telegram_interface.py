import os
import time
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


bot_token = os.environ['AION_BOT_TOKEN']
chat_id = os.environ['TELEGRAM_CHAT_ID']
updater = None
outpipe = None

state = 0

def receive_message(update, context):
    
    #logging it

    r = requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={f"Received message: " + update["message"]["text"]}')
    #print(r.json())
    print(update)

#def send_message(text, )

def error(update, context):
    print('got an error')
    print("\nError: ", context.error)
    print(update)

def shutdown(update, context):
    global outpipe
    print('received shutdown text')
    update.message.reply_text('Shutting down Aion...')
    outpipe.send('/shutdown')

def debug(update, context):
    r = requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={"testing"}')
    print(r.json())
    update.message.reply_text('')




def start(_outpipe, inpipe, arg):
    global state
    global updater, outpipe

    state = arg

    outpipe = _outpipe
    updater = Updater(bot_token, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("shutdown", shutdown))
    dispatcher.add_handler(CommandHandler("debug", debug))
    dispatcher.add_handler(MessageHandler(Filters.all, receive_message))
    dispatcher.add_error_handler(error, True)

    updater.start_polling()
    time.sleep(1)
    print('sendigns')
    outpipe.send('Online')
    try:
        updater.idle([])
    except KeyboardInterrupt:
        print('Shutting down Telegram interface')
        updater.stop()
        print('Telegram interface off')

if __name__ == '__main__':
    start()
