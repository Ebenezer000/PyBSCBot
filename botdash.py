import logging
import secrets
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram.ext import CallbackContext, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
import pytz
import asyncio
from datetime import datetime
############################### Variables ######################################
username = ''
ttkbalance = ''
nath_id = "1375829447"
eben_id = "918895150"
doc_id = "1759671050"
nic_id = "483493043"
adminnumber = 1234567890
################################# Bot ##########################################
def start(update: Update, context: CallbackContext) -> str:
  chat_id = update.effective_chat.id
  user = client.query(q.get(q.match(q.index("name"), chat_id)))
  first_name = update["message"]["chat"]["first_name"]
  last_name = update["message"]["chat"]["last_name"]
  username = first_name+' '+last_name
  try:
      client.query(q.get(q.match(q.index("name"), adminnumber)))
  except:
      user = client.query(q.create(q.collection("Admindata"), {
            "data": {
                "adminnumber": adminnumber,
                "totalusers": 22,
                "totalregistered": 19,
                "Latestusername": "Ebenezer Akpas",
                "latestuseraddress": "",
                "date": Time("2021-07-10T23:54:25.300388Z"),
                "Latestuseraddress": "0x96A514f9b0bEb091f8aEe2404410E6ADd21395f4",
                "date": datetime.now(pytz.UTC)
            }
        }))
  if chat_id == doc_id or chat_id == eben_id:
      context.bot.send_message(chat_id = chat_id, text =('Hi '+username+'\nWelcome to your admin dashboard \nWhat would you like to do today'),
                             reply_markup=admin_menu())
  elif chat_id == nath_id or chat_id == nic_id:
      context.bot.send_message(chat_id = chat_id, text =('Hi '+username+'\nWelcome to your admin dashboard \nWhat would you like to do today'),
                             reply_markup=admin_menu())
  else:
      context.bot.send_message(chat_id = chat_id, text =('Hi '+username+'\nYou are not an admin and you dont have access to this dashboard'))

async def sendupdates(update, context):
     while True:
        # await asyncio.sleep(86400)
        await asyncio.sleep(120)
        admin = client.query(q.get(q.match(q.index("Admindata"), adminnumber)))
        today = str(datetime.now(pytz.UTC))
        latestusername = admin["data"]["Latestusername"]
        latestuseraddress = admin["data"]["latestuseraddress"]
        totalusers = str(admin["data"]["totalusers"])
        context.bot.send_message(chat_id = eben_id, text =('Hi Admin\nBot Update at '+today+'\nThe total number of bot users at the time of this update is: '+totalusers+'\nThe latest registered user has these details\nUsername: '+latestusername+'\nAddress: '+latestuseraddress))
        context.bot.send_message(chat_id = doc_id, text =('Hi Admin\nBot Update at '+today+'\nThe total number of bot users at the time of this update is: '+totalusers+'\nThe latest registered user has these details\nUsername: '+latestusername+'\nAddress: '+latestuseraddress))
        # context.bot.send_message(chat_id = chat_id, text =('Hi '+username+'\nYou are not an admin and you dont have access to this dashboard'))
        # context.bot.send_message(chat_id = chat_id, text =('Hi '+username+'\nYou are not an admin and you dont have access to this dashboard'))

def echo(update, context):
    """Handle direct user messages"""
    chat_id = update.effective_chat.id
    message = update.message.text
    last_command = user["data"]["last_command"]
    first_name = update["message"]["chat"]["first_name"]
    last_name = update["message"]["chat"]["last_name"]
    username = first_name+' '+last_name
    context.bot.send_message(chat_id = chat_id, text =(message+'??,' +username+" I don't understand your message please use the onscreen keybord"))

def error(update, context):
    print(f'Wetin dey sup be sey {context.error}')
############################### Keyboard #######################################
def admin_menu():
    keyboard = [[InlineKeyboardButton('See latest User Details', callback_data='Latestuser')],
                [InlineKeyboardButton('Check Latest bot statistics', callback_data='Botstats')]]
    return InlineKeyboardMarkup(keyboard)
############################### Messages #######################################
def Latestuser(update, context):
    chat_id = update.effective_chat.id
    admin = client.query(q.get(q.match(q.index("Admindata"), adminnumber)))
    latestusername = admin["data"]["Latestusername"]
    latestuseraddress = admin["data"]["latestuseraddress"]
    context.bot.send_message(chat_id = chat_id, text =('The latest registered user has these Details \nFirst Name and Last name:\n'+latestusername+'\nAddress:\n'+latestuseraddress+'\nNOTE: If any entry is left blank this user did not register their telegram account with that field'))

def Botstats(update, context):
    chat_id = update.effective_chat.id
    admin = client.query(q.get(q.match(q.index("Admindata"), adminnumber)))
    today = str(datetime.now(pytz.UTC))
    latestusername = admin["data"]["Latestusername"]
    latestuseraddress = admin["data"]["latestuseraddress"]
    totalusers = str(admin["data"]["totalusers"])
    context.bot.send_message(chat_id = chat_id, text =('Hi Admin\nBot Update at '+today+'\nThe total number of bot users at the time of this update is: '+totalusers+'\nThe latest registered user has these details\nUsername: '+latestusername+'\nAddress: '+latestuseraddress))


############################### Updaters #######################################
"""Start the bot."""
TOKEN = '1893200771:AAHA6QoXLqd7zzFUS43hbfMzRM0Sd4Lsb_w'
fauna_secret ="fnAELmJxylACB_xpdn9C6SNpufVLKB1r5zi7kErv"
updater = Updater(TOKEN, use_context="natrue")
client = FaunaClient(secret=fauna_secret)

loop = asyncio.get_event_loop()
asyncio.ensure_future(sendupdates(TOKEN, updater))
loop.run_forever()

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(Latestuser, pattern='Latestuser'))
updater.dispatcher.add_handler(CallbackQueryHandler(Botstats, pattern='Botstats'))

updater.dispatcher.add_error_handler(error)

# Get the dispatcher to register handlers
dp = updater.dispatcher

# on noncommand i.e message - echo the message on Telegram
dp.add_handler(MessageHandler(Filters.text, echo))

updater.start_polling()

# Run the bot until you press Ctrl-C and will stop the bot gracefully.
updater.idle()
