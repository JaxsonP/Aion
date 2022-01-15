import os
import time
import logging
import telegram
from telegram.ext import *

aion_pipe = None
bot_token = os.environ['AION_BOT_TOKEN']
chat_id = os.environ['TELEGRAM_CHAT_ID']
chat = None

def start(_aion_pipe):
    global aion_pipe, chat
    aion_pipe = _aion_pipe
    chat = telegram.Chat(chat_id, 'private')

    logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', filename='logs\\telegram_interface.log', level=logging.INFO)
    aps_logger = logging.getLogger('apscheduler')
    aps_logger.setLevel(logging.WARNING)


    updater = Updater(bot_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("shutdown", shutdown))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), receive_message))
    #dispatcher.add_error_handler(error, True)

    updater.start_polling()
    updater.idle()

def receive_message(update, context):
    print("Received telegram message")
    #display_typing()
    aion_pipe.send(update.message.text)

def display_typing():
    #global bot
    chat.send_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)

def error(update, context):
    print("Received Error: ", update)

def shutdown(update, context):
    aion_pipe.send('/shutdown')
    aion_pipe.close()
    pass

"""
EXAMPLE UPDATE":
{
   "message":{
      "text":"Tgst",
      "message_id":60,
      "caption_entities":[
         
      ],
      "chat":{
         "first_name":"Jaxson",
         "id":1948408284,
         "username":"jaxsonp",
         "last_name":"P",
         "type":"private"
      },
      "photo":[
         
      ],
      "new_chat_members":[
         
      ],
      "entities":[
         
      ],
      "date":1642280885,
      "channel_chat_created":false,
      "supergroup_chat_created":false,
      "new_chat_photo":[
         
      ],
      "delete_chat_photo":false,
      "group_chat_created":false,
      "from":{
         "is_bot":false,
         "id":1948408284,
         "last_name":"P",
         "first_name":"Jaxson",
         "username":"jaxsonp",
         "language_code":"en"
      }
   },
   "update_id":239026697
}
"""