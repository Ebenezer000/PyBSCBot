import logging
import secrets
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram.ext import CallbackContext, MessageHandler, Filters, ChatMemberHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Chat, ChatMember, ParseMode, ChatMemberUpdated
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
from lxml import html
from bs4 import BeautifulSoup
import requests
import pytz
import Botabi
from datetime import datetime
from web3 import Web3
from hexbytes import HexBytes
from web3.middleware import construct_sign_and_send_raw_middleware
import os
############################### Logging ########################################

# get the heroku port
PORT = int(os.environ.get('PORT', 8443) )

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org:443'))
################################ Variables #####################################
username = ''
password = ''
first_name = ''
last_name = ''
collector = '0x46Ae707B2CcE0AB634551f4Fb58E2d9E18210b87'
Owner = '0x000000000000000000000000000000000000dEaD'
website = 'https://www.ttk.finance'
chasher ='https://bscscan.com/tx/'
hash_link = 'https://bscscan.com'
TOKEN = '1877580174:AAEd0xkWtccSDFmr4bo0VSbdP2yI7CI-I40'
fauna_secret ="fnAELmJxylACB_xpdn9C6SNpufVLKB1r5zi7kErv"
eben_id = '918895150'
doc_id = '1759671050'
adminnumber = 1234567890

################################# Tokens #######################################
TTK = Botabi.ttkabi
BUSD = Botabi.busdabi
USDT = Botabi.usdtabi
TTKRAIN = Botabi.rainabi
rain_address = Web3.toChecksumAddress('0x0E51d0ee4c5ec0CEd2375CbBD336D86675De182A')
ttk_address = Web3.toChecksumAddress('0x9b6ad26568e7E3cE9670487bf7a32b2c9f34b142')
busd_address = Web3.toChecksumAddress('0xe9e7cea3dedca5984780bafc599bd69add087d56')
usdt_address = Web3.toChecksumAddress('0x55d398326f99059ff775485246999027b3197955')
raincontract = w3.eth.contract(rain_address, abi=TTKRAIN)
ttkcontract = w3.eth.contract(ttk_address, abi=TTK)
busdcontract = w3.eth.contract(busd_address, abi=BUSD)
usdtcontract = w3.eth.contract(usdt_address, abi=USDT)
############################# Crypto Variiables ################################
address = ''
shareamount = int(0)
bnbpage = requests.get('https://coinmarketcap.com/currencies/binance-coin')
btcpage = requests.get('https://www.coindesk.com/price/bitcoin')
ethpage = requests.get('https://coinmarketcap.com/currencies/ethereum')
bnbtree = html.fromstring(bnbpage.content)
btctree = html.fromstring(btcpage.content)
ethtree = html.fromstring(ethpage.content)
_bnbprice = str(bnbtree.xpath('//div[@class="priceValue___11gHJ"]/text()'))
_btcprice = str(btctree.xpath('//div[@class="price-large"]/text()'))
_ethprice = str(ethtree.xpath('//div[@class="priceValue___11gHJ"]/text()'))
_btc_price_ = _btcprice[1]
bnb_price = _bnbprice.strip(" [''] ")
btc_price = _btcprice.strip(" [''] ")
eth_price = _ethprice.strip(" [''] ")
KEY = ''
################################### Bot ########################################
################################# Commands #####################################
def start(update: Update, context: CallbackContext) -> str:
  chat_id = update.effective_chat.id
  admin = client.query(q.get(q.match(q.index("Admindata"), adminnumber)))
  totalusers = admin["data"]["totalusers"]
  try:
    first_name = update["message"]["chat"]["first_name"]
    last_name = update["message"]["chat"]["last_name"]
    username = first_name+' '+last_name
    try:
        client.query(q.get(q.match(q.index("name"), chat_id)))
    except:
        try:
            userstotal = totalusers + 1
            user = client.query(q.create(q.collection("Login-details"), {
                  "data": {
                      "id": chat_id,
                      "first_name": first_name,
                      "username": username,
                      "last_command": "",
                      "signed_up": "",
                      "logged_in": "dids",
                      "password" : "",
                      "address" : "",
                      "private-key": "",
                      "transfer-type": "",
                      "date": datetime.now(pytz.UTC)
                  }
              }))
            client.query(q.update(q.ref(q.collection("UserUpdates"), adminnumber), {"data": {"totalusers": userstotal}}))
        except:
            pass

  except:
    try:
        client.query(q.get(q.match(q.index("name"), chat_id)))
    except:
        try:
            userstotal = totalusers + 1
            user = client.query(q.create(q.collection("Login-details"), {
                  "data": {
                      "id": chat_id,
                      "last_command": "",
                      "signed_up": "",
                      "logged_in": "dids",
                      "password" : "",
                      "address" : "",
                      "private-key": "",
                      "transfer-type": "",
                      "date": datetime.now(pytz.UTC)
                  }
              }))
            client.query(q.update(q.ref(q.collection("UserUpdates"), adminnumber), {"data": {"totalusers": userstotal}}))
        except:
            pass
  context.bot.send_message(chat_id = chat_id, text =('Hello '+username+',\n\nWelcome to the BSC Telegram BOT powered by TTK,\n\n-To SignUp for your Wallet or veiw your Private Key click Account.\n-To Deposit, Transfer and Withdraw Click on Finances.'),
                     reply_markup=main_menu_keyboard())

def help(update: Update, context: CallbackContext) -> str:
    if chat.type == Chat.PRIVATE:
        chat_id = update.effective_chat.id
        try:
            user = client.query(q.get(q.match(q.index("name"), chat_id)))
            using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
            username=using["data"]["username"]
        except:
            username = ''
        context.bot.send_message(chat_id = chat_id, text = 'Hi '+username+'\n\nThis is a help message from the BSC Telegram BOT powered by TTK\n Here we will guide you through the use of this bot.\n\n This bot can be utilized in two ways\n1. With an on screen keybord\n 2. With direct commands\n One example of that command is the /help comand \n our list of commands can be seen through the menu button and are explained here\n/deposit\nThis displays your deposit address\n/transfer\n This function activates when used in this format\n/transfer <address> <amount> <symbol>\nFor Example\n/transfer 0x000000000000000000000000000000000000000D 100 TTK \n\n/balance\n Shows the total amount of TTK, BNB, BUSD and USDT in your account \n/price \nThis displays the current prices of BTC, ETH and BNB')
    elif chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
        sender = update.effective_user.id
        try:
            user = client.query(q.get(q.match(q.index("name"), sender)))
            using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
            username=using["data"]["username"]
        except:
            username = ''
            context.bot.send_message(chat_id = chat_id, text = 'Hello\n Help has been sent to you privately')
            context.bot.send_message(chat_id = sender, text = 'Hi '+username+'\n\nThis is a help message from the BSC Telegram BOT powered by TTK\n Here we will guide you through the use of this bot.\n\n This bot can be utilized in two ways\n1. With an on screen keybord\n 2. With direct commands\n One example of that command is the /help comand \n our list of commands can be seen through the menu button and are explained here\n/deposit\nThis displays your deposit address\n/transfer\n This function activates when used in this format\n/transfer <address> <amount> <symbol>\nFor Example\n/transfer 0x000000000000000000000000000000000000000D 100 TTK \n\n/balance\n Shows the total amount of TTK, BNB, BUSD and USDT in your account \n/price \nThis displays the current prices of BTC, ETH and BNB')
    else:
        pass

######## Odd transfer ########
def oddtransfer(update, context):
    chat_id = update.effective_chat.id
    chat = update.effective_chat
    global hash_link
    allowance = int(200000*10**18)
    if chat.type == Chat.PRIVATE:
        user = client.query(q.get(q.match(q.index("name"), chat_id)))
        using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
        password = using["data"]["password"]
        private_key=using["data"]["private-key"]
        Owner = using["data"]["address"]
        try:
            using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
            username=using["data"]["username"]
        except:
            username = ''
        if password == "":
            context.bot.send_message(chat_id = chat_id, text =(username+' You cannot make a transfer without signing up'),
            reply_markup=first_menu_keyboard())
        else:
            try:
                command = context.args[2].upper()
                amount = float(context.args[1])* 10 ** 18
                address = context.args[0]
                if("TTK" == command):
                    upamnt = int(amount)
                    profit = int(fee)
                    gas_required = int(2537000000000000)
                    bnb_balance = int(w3.eth.get_balance(Owner))
                    balance = int(ttkcontract.functions.balanceOf(Owner).call())
                    ttkbalance = int(ttkcontract.functions.balanceOf(Owner).call())
                    if ttkbalance > allowance:
                        if bnb_balance > gas_required:
                            if balance < main:
                                context.bot.send_message(chat_id = chat_id, text = 'You dont have enough TTK to send right now')
                            else:
                                try:
                                    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
                                    w3.eth.default_account = Owner
                                    tx_hash = ttkcontract.functions.transfer(address, upamnt).transact({'from': w3.eth.defaultAccount})
                                    strtx = HexBytes.hex(tx_hash)
                                    hash_link =chasher+strtx
                                    context.bot.send_message(chat_id = chat_id, text = ('TRANSFER SUCCESSFUL!!\n\nTransaction Hash:\n'+strtx),
                                    reply_markup=transdone())
                                except:
                                    context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\nThere seems to be a problem with your input, please retry'),
                                    reply_markup=balmenu())
                        else:
                            context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.002537 BNB'),
                            reply_markup=balmenu())
                    else:
                        context.bot.send_message(chat_id = chat_id, text = ("You don't seem to have enough TTK in your account. Each user is required to have at least 200,000 TTK before transactions can work"),
                        reply_markup=balmenu())

                elif("BNB" == command):
                    upamnt = int(amount)
                    gas_required = int(210000000000000)
                    bnb_balance = int(w3.eth.get_balance(Owner))
                    balance = int(w3.eth.get_balance(Owner))
                    ttkbalance = int(ttkcontract.functions.balanceOf(Owner).call())
                    if ttkbalance > allowance:
                        if bnb_balance > gas_required:
                            if balance < main:
                                context.bot.send_message(chat_id = chat_id, text = 'You dont have enough BNB to send')
                            else:
                                try:
                                    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
                                    w3.eth.default_account = Owner
                                    tx_hash = w3.eth.send_transaction({'to': address, 'from': w3.eth.defaultAccount, 'value': upamnt})
                                    strtx = HexBytes.hex(tx_hash)
                                    hash_link =chasher+strtx
                                    context.bot.send_message(chat_id = chat_id, text = ('TRANSFER SUCCESSFUL!!\n\nTransaction Hash:\n'+strtx),
                                    reply_markup=transdone())
                                except:
                                    context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\nThere seems to be a problem with your input, please retry'),
                                    reply_markup=balmenu())
                        else:
                            context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.000210 BNB'),
                            reply_markup=balmenu())
                    else:
                        context.bot.send_message(chat_id = chat_id, text = ("You don't seem to have enough TTK in your account. Each user is required to have at least 200,000 TTk before transactions can work"),
                        reply_markup=balmenu())

                elif("BUSD" == command):
                    upamnt = int(amount)
                    gas_required = int(5037000000000000)
                    bnb_balance = int(w3.eth.get_balance(Owner))
                    balance = int(busdcontract.functions.balanceOf(Owner).call())
                    ttkbalance = int(ttkcontract.functions.balanceOf(Owner).call())
                    if ttkbalance > allowance:
                        if bnb_balance > gas_required:
                            if balance < main:
                                context.bot.send_message(chat_id = chat_id, text = 'You dont have enough BUSD to send')
                            else:
                                try:
                                    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
                                    w3.eth.default_account = Owner
                                    tx_hash = busdcontract.functions.transfer(address, upamnt).transact({'from': w3.eth.defaultAccount})
                                    strtx = HexBytes.hex(tx_hash)
                                    hash_link =chasher+strtx
                                    context.bot.send_message(chat_id = chat_id, text = ('TRANSFER SUCCESSFUL!!\n\nTransaction Hash:\n'+strtx),
                                    reply_markup=transdone())
                                except:
                                    context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\nThere seems to be a problem with your input, please retry'),
                                    reply_markup=balmenu())
                        else:
                            context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.005037 BNB'),
                            reply_markup=balmenu())
                    else:
                        context.bot.send_message(chat_id = chat_id, text = ("You don't seem to have enough TTK in your account. Each user is required to have at least 200,000 TTk before transactions can work"),
                        reply_markup=balmenu())

                elif("USDT" == command):
                    upamnt = int(amount)
                    gas_required = int(5037000000000000)
                    bnb_balance = int(w3.eth.get_balance(Owner))
                    balance = int(usdtcontract.functions.balanceOf(Owner).call())
                    ttkbalance = int(ttkcontract.functions.balanceOf(Owner).call())
                    if ttkbalance > allowance:
                        if bnb_balance > gas_required:
                            if balance < main:
                                context.bot.send_message(chat_id = chat_id, text = 'You dont have enough USDT to send')
                            else:
                                try:
                                    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
                                    w3.eth.default_account = Owner
                                    tx_hash = usdtcontract.functions.transfer(address, upamnt).transact({'from': w3.eth.defaultAccount})
                                    strtx = HexBytes.hex(tx_hash)
                                    hash_link =chasher+strtx
                                    context.bot.send_message(chat_id = chat_id, text = ('TRANSFER SUCCESSFUL!!\n\nTransaction Hash:\n'+strtx),
                                    reply_markup=transdone())
                                except:
                                    context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\nThere seems to be a problem with your input, please retry'),
                                    reply_markup=balmenu())
                        else:
                            context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.005037 BNB'),
                            reply_markup=balmenu())
                    else:
                        context.bot.send_message(chat_id = chat_id, text = ("You don't seem to have enough TTK in your account. Each user is required to have at least 200,000 TTk before transactions can work"),
                        reply_markup=balmenu())
            except:
                context.bot.send_message(chat_id = chat_id, text = "/transfer\n This function activates when used in this format\n/transfer <address> <amount> <symbol>\nFor Example\n /transfer 0x0000000000000000000000000000000000000000 100 TTK")
    elif chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
        sender = update.effective_user.id
        user = client.query(q.get(q.match(q.index("name"), sender)))
        using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
        password = using["data"]["password"]
        private_key=using["data"]["private-key"]
        Owner = using["data"]["address"]
        try:
            username=using["data"]["username"]
        except:
            username = ''
        if password == "":
            context.bot.send_message(chat_id = chat_id, text =('You cannot Rain tokens without signing up'))
            context.bot.send_message(chat_id = sender, text =('You have not signed up for this service'),reply_markup=first_menu_keyboard())
        else:
            try:
                command = context.args[2].upper()
                amount = float(context.args[1])* 10 ** 18
                address = context.args[0]
                if("TTK" == command):
                    upamnt = int(amount)
                    gas_required = int(2537000000000000)
                    bnb_balance = int(w3.eth.get_balance(Owner))
                    balance = int(ttkcontract.functions.balanceOf(Owner).call())
                    ttkbalance = int(ttkcontract.functions.balanceOf(Owner).call())
                    if ttkbalance > allowance:
                        if bnb_balance > gas_required:
                            if balance < upamnt:
                                context.bot.send_message(chat_id = chat_id, text = 'Your TTK balance is not up to '+context.args[1])
                            else:
                                try:
                                    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
                                    w3.eth.default_account = Owner
                                    tx_hash = ttkcontract.functions.transfer(address, upamnt).transact({'from': w3.eth.defaultAccount})
                                    strtx = HexBytes.hex(tx_hash)
                                    hash_link =chasher+strtx
                                    context.bot.send_message(chat_id = chat_id, text = ('TRANSFER SUCCESSFUL!!\n\nTransaction Hash:\n'+strtx),
                                    reply_markup=transdone())
                                except:
                                    context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\nThere seems to be a problem with your input, please retry'),
                                    reply_markup=balmenu())
                        else:
                            context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.002537 BNB'),
                            reply_markup=balmenu())
                    else:
                        context.bot.send_message(chat_id = chat_id, text = ("You don't seem to have enough TTK in your account. Each user is required to have at least 200,000 TTK before transactions can work"),
                        reply_markup=balmenu())

                elif("BNB" == command):
                    upamnt = int(amount)
                    gas_required = int(210000000000000)
                    bnb_balance = int(w3.eth.get_balance(Owner))
                    balance = int(w3.eth.get_balance(Owner))
                    ttkbalance = int(ttkcontract.functions.balanceOf(Owner).call())
                    if ttkbalance > allowance:
                        if bnb_balance > gas_required:
                            if balance < upamnt:
                                context.bot.send_message(chat_id = chat_id, text = 'You dont have enough BNB to send')
                            else:
                                try:
                                    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
                                    w3.eth.default_account = Owner
                                    tx_hash = w3.eth.send_transaction({'to': address, 'from': w3.eth.defaultAccount, 'value': upamnt})
                                    strtx = HexBytes.hex(tx_hash)
                                    hash_link =chasher+strtx
                                    context.bot.send_message(chat_id = chat_id, text = ('TRANSFER SUCCESSFUL!!\n\nTransaction Hash:\n'+strtx),
                                    reply_markup=transdone())
                                except:
                                    context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\nThere seems to be a problem with your input, please retry'),
                                    reply_markup=balmenu())
                        else:
                            context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.000210 BNB'),
                            reply_markup=balmenu())
                    else:
                        context.bot.send_message(chat_id = chat_id, text = ("You don't seem to have enough TTK in your account. Each user is required to have at least 200,000 TTk before transactions can work"),
                        reply_markup=balmenu())

                elif("BUSD" == command):
                    upamnt = int(amount)
                    gas_required = int(5037000000000000)
                    bnb_balance = int(w3.eth.get_balance(Owner))
                    balance = int(busdcontract.functions.balanceOf(Owner).call())
                    ttkbalance = int(ttkcontract.functions.balanceOf(Owner).call())
                    if ttkbalance > allowance:
                        if bnb_balance > gas_required:
                            if balance < upamnt:
                                context.bot.send_message(chat_id = chat_id, text = 'You dont have enough BUSD to send')
                            else:
                                try:
                                    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
                                    w3.eth.default_account = Owner
                                    tx_hash = busdcontract.functions.transfer(address, upamnt).transact({'from': w3.eth.defaultAccount})
                                    strtx = HexBytes.hex(tx_hash)
                                    hash_link =chasher+strtx
                                    context.bot.send_message(chat_id = chat_id, text = ('TRANSFER SUCCESSFUL!!\n\nTransaction Hash:\n'+strtx),
                                    reply_markup=transdone())
                                except:
                                    context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\nThere seems to be a problem with your input, please retry'),
                                    reply_markup=balmenu())
                        else:
                            context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.005037 BNB'),
                            reply_markup=balmenu())
                    else:
                        context.bot.send_message(chat_id = chat_id, text = ("You don't seem to have enough TTK in your account. Each user is required to have at least 200,000 TTk before transactions can work"),
                        reply_markup=balmenu())

                elif("USDT" == command):
                    upamnt = int(amount)
                    gas_required = int(5037000000000000)
                    bnb_balance = int(w3.eth.get_balance(Owner))
                    balance = int(usdtcontract.functions.balanceOf(Owner).call())
                    ttkbalance = int(ttkcontract.functions.balanceOf(Owner).call())
                    if ttkbalance > allowance:
                        if bnb_balance > gas_required:
                            if balance < upamnt:
                                context.bot.send_message(chat_id = chat_id, text = 'You dont have enough USDT to send')
                            else:
                                try:
                                    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
                                    w3.eth.default_account = Owner
                                    tx_hash = usdtcontract.functions.transfer(address, upamnt).transact({'from': w3.eth.defaultAccount})
                                    strtx = HexBytes.hex(tx_hash)
                                    hash_link =chasher+strtx
                                    context.bot.send_message(chat_id = chat_id, text = ('TRANSFER SUCCESSFUL!!\n\nTransaction Hash:\n'+strtx),
                                    reply_markup=transdone())
                                except:
                                    context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\nThere seems to be a problem with your input, please retry'),
                                    reply_markup=balmenu())
                        else:
                            context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.005037 BNB'),
                            reply_markup=balmenu())
                    else:
                        context.bot.send_message(chat_id = chat_id, text = ("You don't seem to have enough TTK in your account. Each user is required to have at least 200,000 TTk before transactions can work"),
                        reply_markup=balmenu())
            except:
                context.bot.send_message(chat_id = chat_id, text = "/transfer\n This function activates when used in this format\n/transfer <address> <amount> <symbol>\nFor Example\n /transfer 0x0000000000000000000000000000000000000000 100 TTK")
    else:
        pass
                
######## Odd transfer ##########################################################

######## Odd Rain ##############################################################
def rain(update, context):
    chat_id = update.effective_chat.id
    chat = update.effective_chat
    global hash_link
    allowance = int(200000*10**18)
    approveamount = 1000**10
    if chat.type == Chat.PRIVATE:
        user = client.query(q.get(q.match(q.index("name"), chat_id)))
        using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
        password = using["data"]["password"]
        private_key=using["data"]["private-key"]
        Owner = using["data"]["address"]
        try:
            username=using["data"]["username"]
        except:
            username = ''
        if password == "":
            context.bot.send_message(chat_id = chat_id, text =(username+' You cannot make a Rain tokens without signing up'))
        else:
            try:
                command = context.args[2].upper()
                ramount =  int(context.args[1])
                rusers = int(context.args[0])
                users = context.args[1]
                amount = context.args[0]
                if("TTK" == command):
                    gas_required = int(1537000000000000)
                    bnb_balance = int(w3.eth.get_balance(Owner))
                    balance = int(ttkcontract.functions.balanceOf(Owner).call())
                    if bnb_balance > gas_required:
                        if balance < amount:
                            context.bot.send_message(chat_id = chat_id, text = ('Your TTK balance is not enough to rain '+context.args[0]+' TTK'))
                        else:
                            try:
                                w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
                                w3.eth.default_account = Owner
                                ttkcontract.functions.approve(rain_address, approveamount).transact({'from': w3.eth.defaultAccount})
                                raincontract.functions.createRain(ramount, rusers, ttk_address).transact({'from': w3.eth.defaultAccount})
                                context.bot.send_message(chat_id = chat_id, text =('CREATION SUCCESSFUL\n\nThis rain was created for '+users+' users'))
                            except:
                                context.bot.send_message(chat_id = chat_id, text = ('CREATION FAILED\nThere seems to be a problem with your input, please retry'))
                    else:
                        context.bot.send_message(chat_id = chat_id, text = ('CREATION FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.001537 BNB'))

                elif("USDT" == command):
                    gas_required = int(1537000000000000)
                    bnb_balance = int(w3.eth.get_balance(Owner))
                    balance = int(usdtcontract.functions.balanceOf(Owner).call())
                    if bnb_balance > gas_required:
                        if balance < amount:
                            context.bot.send_message(chat_id = chat_id, text = ('Your USDT balance is not enough to rain '+context.args[0]+' USDT'))
                        else:
                            try:
                                w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
                                w3.eth.default_account = Owner
                                usdtcontract.functions.approve(rain_address, approveamount).transact({'from': w3.eth.defaultAccount})
                                raincontract.functions.createRain(ramount, rusers, usdt_address).transact({'from': w3.eth.defaultAccount})
                                context.bot.send_message(chat_id = chat_id, text = ('CREATION SUCCESSFUL\n\nThis rain was created for '+users+' users'))
                            except:
                                context.bot.send_message(chat_id = chat_id, text = ('CREATION FAILED\nThere seems to be a problem with your input, please retry'))
                    else:
                        context.bot.send_message(chat_id = chat_id, text = ('CREATION FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.001537 BNB'))

                elif("BUSD" == command):
                    gas_required = int(1537000000000000)
                    bnb_balance = int(w3.eth.get_balance(Owner))
                    balance = int(busdcontract.functions.balanceOf(Owner).call())
                    if bnb_balance > gas_required:
                        if balance < amount:
                            context.bot.send_message(chat_id = chat_id, text = ('Your BUSD balance is not enough to rain '+context.args[0]+' BUSD'))
                        else:
                            try:
                                w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
                                w3.eth.default_account = Owner
                                busdcontract.functions.approve(rain_address, approveamount).transact({'from': w3.eth.defaultAccount})
                                raincontract.functions.createRain(ramount, rusers, busd_address).transact({'from': w3.eth.defaultAccount})
                                context.bot.send_message(chat_id = chat_id, text = ('CREATION SUCCESSFUL\n\nThis rain was created for '+users+' users'))
                            except:
                                context.bot.send_message(chat_id = chat_id, text = ('CREATION FAILED\nThere seems to be a problem with your input, please retry'))
                    else:
                        context.bot.send_message(chat_id = chat_id, text = ('CREATION FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.001537 BNB'))
            except:
                context.bot.send_message(chat_id = chat_id, text = "/rain\n This function activates when used in this format\n/rain <amount> <users> <symbol>\nFor Example:\n /rain 50 10 TTK\n50ttk will be shared among 10 users")

    elif chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
        sender = update.effective_user.id
        user = client.query(q.get(q.match(q.index("name"), sender)))
        using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
        password = using["data"]["password"]
        private_key=using["data"]["private-key"]
        Owner = using["data"]["address"]
        try:
            username= update.effective_user.first_name
        except:
            username = 'A user'
        if password == "":
            context.bot.send_message(chat_id = chat_id, text =('You cannot Rain tokens without signing up'))
            context.bot.send_message(chat_id = sender, text =('You have not signed up for this service'),reply_markup=first_menu_keyboard())
        else:
            try:
                command = context.args[2].upper()
                users = context.args[1]
                amount = context.args[0]
                if("TTK" == command):
                    gas_required = int(1537000000000000)
                    bnb_balance = int(w3.eth.get_balance(Owner))
                    balance = int(ttkcontract.functions.balanceOf(Owner).call())
                    if bnb_balance > gas_required:
                        if balance < amount:
                            context.bot.send_message(chat_id = chat_id, text = ('Your TTK balance is not enough to rain '+context.args[0]+' TTK'))
                        else:
                            try:
                                w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
                                w3.eth.default_account = Owner
                                ttkcontract.functions.approve(rain_address, approveamount).transact({'from': w3.eth.defaultAccount})
                                raincontract.functions.createRain(amount, user, ttk_address).transact({'from': w3.eth.defaultAccount})
                                context.bot.send_message(chat_id = chat_id, text =('A '+command+' Rain has been created by '+username+' for '+users+' users\nYou can now claim this rain privately from your wallet'))
                            except:
                                context.bot.send_message(chat_id = chat_id, text = ('CREATION FAILED\nThere seems to be a problem with your input, please retry'))
                    else:
                        context.bot.send_message(chat_id = sender, text = ('CREATION FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.001537 BNB'))

                elif("USDT" == command):
                    gas_required = int(1537000000000000)
                    bnb_balance = int(w3.eth.get_balance(Owner))
                    balance = int(usdtcontract.functions.balanceOf(Owner).call())
                    if bnb_balance > gas_required:
                        if balance < amount:
                            context.bot.send_message(chat_id = chat_id, text = ('Your USDT balance is not enough to rain '+context.args[0]+' USDT'))
                        else:
                            try:
                                w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
                                w3.eth.default_account = Owner
                                usdtcontract.functions.approve(rain_address, approveamount).transact({'from': w3.eth.defaultAccount})
                                raincontract.functions.createRain(amount, user, usdt_address).transact({'from': w3.eth.defaultAccount})
                                context.bot.send_message(chat_id = chat_id, text = ('A '+command+' Rain has been created by '+username+' for '+users+' users\nYou can now claim this rain privately from your wallet'))
                            except:
                                context.bot.send_message(chat_id = chat_id, text = ('CREATION FAILED\nThere seems to be a problem with your input, please retry'))
                    else:
                        context.bot.send_message(chat_id = chat_id, text = ('CREATION FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.001537 BNB'))

                elif("BUSD" == command):
                    gas_required = int(1537000000000000)
                    bnb_balance = int(w3.eth.get_balance(Owner))
                    balance = int(busdcontract.functions.balanceOf(Owner).call())
                    if bnb_balance > gas_required:
                        if balance < amount:
                            context.bot.send_message(chat_id = chat_id, text = ('Your BUSD balance is not enough to rain '+context.args[0]+' BUSD'))
                        else:
                            try:
                                w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
                                w3.eth.default_account = Owner
                                busdcontract.functions.approve(rain_address, approveamount).transact({'from': w3.eth.defaultAccount})
                                raincontract.functions.createRain(amount, user, busd_address).transact({'from': w3.eth.defaultAccount})
                                context.bot.send_message(chat_id = chat_id, text = ('A '+command+' Rain has been created by '+username+' for '+users+' users\nYou can now claim this rain privately from your wallet'))
                            except:
                                context.bot.send_message(chat_id = chat_id, text = ('CREATION FAILED\nThere seems to be a problem with your input, please retry'))
                    else:
                        context.bot.send_message(chat_id = chat_id, text = ('CREATION FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.001537 BNB'))
            except:
                context.bot.send_message(chat_id = chat_id, text = "/rain\n This function activates when used in this format\n/rain <amount> <users> <symbol>\nFor Example:\n /rain 50 10 TTK\n50ttk will be shared among 10 users")
    else:
        pass
######## Odd Rain ##############################################################


def deposit(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    chat_id = update.effective_chat.id
    if chat.type == Chat.PRIVATE:
        user = client.query(q.get(q.match(q.index("name"), chat_id)))
        using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
        try:
            username=using["data"]["username"]
        except:
            username = ''
        address = using["data"]["address"]
        password = using["data"]["password"]
        if chat.type == Chat.PRIVATE:
            if password == "":
                context.bot.send_message(chat_id = chat_id, text = 'You cannot view your deposit address without signing up')
            else:
                context.bot.send_message(chat_id = chat_id, text = ('Hi '+username+'\nYour Deposit Address:\n'+address+'\nNOTE:\nThis address can only recieve TTK, BNB, BUSD and USDT(BEP20)'),
                reply_markup=back_to_main())
    elif chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
        sender = update.effective_user.id
        user = client.query(q.get(q.match(q.index("name"), sender)))
        using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
        try:
            username=using["data"]["username"]
        except:
            username = ''
        address = using["data"]["address"]
        password = using["data"]["password"]
        if password == "":
            context.bot.send_message(chat_id = chat_id, text = 'You have not signed up for this service')
            context.bot.send_message(chat_id = sender, text = 'You can only have full access to this service by signing up')
        else:
            context.bot.send_message(chat_id = chat_id, text = 'Hi '+username+'\nYour Deposit Address:\n'+address+'\nNOTE:\nThis address can only recieve TTK, BNB, BUSD and USDT(BEP20)')
            context.bot.send_message(chat_id = sender, text = 'Your deposit address was just shared on a public group')
    else:
        pass
############################## Bot Remaining ###################################


def main_menu(bot, update):
  bot.callback_query.message.edit_text(main_menu_message(),
                          reply_markup=main_menu_keyboard())

def first_menu(bot, update):
  bot.callback_query.message.edit_text(first_menu_message(),
                          reply_markup=first_menu_keyboard())

def second_menu(bot, update):
  bot.callback_query.message.edit_text(second_menu_message(),
                          reply_markup=second_menu_keyboard())

def first_submenu(bot, update):
  pass

def second_submenu(bot, update):
  pass


def echo(update, context):
    """Handle direct user messages"""
    chat_id = update.effective_chat.id
    chat = update.effective_chat
    message = update.message.text
    global hash_link
    global address
    global shareamount
    user = client.query(q.get(q.match(q.index("name"), chat_id)))
    using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
    last_command = using["data"]["last_command"]
    private_key=using["data"]["private-key"]
    transfer_type =using["data"]["transfer-type"]
    Owner = using["data"]["address"]
    allowance = int(200000*10**18)
    try:
        using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
        username=using["data"]["username"]
    except:
        username = ''
    if last_command == "address":
        global address
        address = str(update.message.text)
        client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"last_command": "amount"}}))
        context.bot.send_message(chat_id = chat_id, text = 'How much would you like to transfer to this address ['+address+']')

    elif last_command == "amount":
        client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"last_command": ""}}))
        amount = float(update.message.text)* 10 ** 18
        if transfer_type == "ttk":
            client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"transfer-type": ""}}))
            upamnt = int(amount)
            gas_required = int(5037000000000000)
            bnb_balance = int(w3.eth.get_balance(Owner))
            balance = int(ttkcontract.functions.balanceOf(Owner).call())
            ttkbalance = int(ttkcontract.functions.balanceOf(Owner).call())
            if ttkbalance > allowance:
                if bnb_balance > gas_required:
                    if balance < main:
                        context.bot.send_message(chat_id = chat_id, text = 'You dont have enough TTK to send right now')
                    else:
                        try:
                            w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
                            w3.eth.default_account = Owner
                            tx_hash = ttkcontract.functions.transfer(address, upamnt).transact({'from': w3.eth.defaultAccount})
                            strtx = HexBytes.hex(tx_hash)
                            hash_link =chasher+strtx
                            context.bot.send_message(chat_id = chat_id, text = ('TRANSFER SUCCESSFUL!!\n\nTransaction Hash:\n'+strtx),
                            reply_markup=transdone())
                        except:
                            context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\nThere seems to be a problem with your network connection, please try again later'),
                            reply_markup=balmenu())
                else:
                    context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.005037 BNB'),
                    reply_markup=balmenu())

            else:
                context.bot.send_message(chat_id = chat_id, text = ("You don't seem to have enough TTK in your account. Each user is required to have at least 200,000 TTK before transactions can work"),
                reply_markup=balmenu())

        elif transfer_type == "bnb":
            client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"transfer-type": ""}}))
            upamnt = int(amount)
            balance = int(w3.eth.get_balance(Owner))
            gas_required = int(210000000000000)
            ttkbalance = int(ttkcontract.functions.balanceOf(Owner).call())
            if ttkbalance > allowance:
                if balance > gas_required:
                    if balance < main:
                        context.bot.send_message(chat_id = chat_id, text = 'You dont have enough BNB to send')
                    else:
                        try:
                            w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
                            w3.eth.default_account = Owner
                            tx_hash = w3.eth.send_transaction({'to': address, 'from': w3.eth.defaultAccount, 'value': upamnt})
                            strtx = HexBytes.hex(tx_hash)
                            hash_link =chasher+strtx
                            context.bot.send_message(chat_id = chat_id, text = ('TRANSFER SUCCESSFUL!!\n\nTransaction Hash:\n'+strtx),
                            reply_markup=transdone())
                        except:
                            context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\nThere seems to be a problem with your network connection, please try again later'),
                            reply_markup=balmenu())
                else:
                    context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.004240 BNB'),
                    reply_markup=balmenu())
            else:
                context.bot.send_message(chat_id = chat_id, text = ("You don't seem to have enough TTK in your account. Each user is required to have at least 200,000 TTk before transactions can work"),
                reply_markup=balmenu())

        elif transfer_type == "busd":
            client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"transfer-type": ""}}))
            upamnt = int(amount)
            gas_required = int(5037000000000000)
            bnb_balance = int(w3.eth.get_balance(Owner))
            balance = int(busdcontract.functions.balanceOf(Owner).call())
            ttkbalance = int(ttkcontract.functions.balanceOf(Owner).call())
            if ttkbalance > allowance:
                if bnb_balance > gas_required:
                    if balance < main:
                        context.bot.send_message(chat_id = chat_id, text = 'You dont have enough BUSD to send')
                    else:
                        try:
                            w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
                            w3.eth.default_account = Owner
                            tx_hash = busdcontract.functions.transfer(address, upamnt).transact({'from': w3.eth.defaultAccount})
                            strtx = HexBytes.hex(tx_hash)
                            hash_link =chasher+strtx
                            context.bot.send_message(chat_id = chat_id, text = ('TRANSFER SUCCESSFUL!!\n\nTransaction Hash:\n'+strtx),
                            reply_markup=transdone())
                        except:
                            context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\nThere seems to be a problem with your network connection, please try again later'),
                            reply_markup=balmenu())
                else:
                    context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.005037 BNB'),
                    reply_markup=balmenu())
            else:
                context.bot.send_message(chat_id = chat_id, text = ("You don't seem to have enough TTK in your account. Each user is required to have at least 200,000 TTk before transactions can work"),
                reply_markup=balmenu())

        elif transfer_type == "usdt":
            client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"transfer-type": ""}}))
            upamnt = int(amount)
            gas_required = int(5037000000000000)
            bnb_balance = int(w3.eth.get_balance(Owner))
            balance = int(usdtcontract.functions.balanceOf(Owner).call())
            ttkbalance = int(ttkcontract.functions.balanceOf(Owner).call())
            if ttkbalance > allowance:
                if bnb_balance > gas_required:
                    if balance < main:
                        context.bot.send_message(chat_id = chat_id, text = 'You dont have enough USDT to send')
                    else:
                        try:
                            w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
                            w3.eth.default_account = Owner
                            tx_hash = usdtcontract.functions.transfer(address, upamnt).transact({'from': w3.eth.defaultAccount})
                            strtx = HexBytes.hex(tx_hash)
                            hash_link =chasher+strtx
                            context.bot.send_message(chat_id = chat_id, text = ('TRANSFER SUCCESSFUL!!\n\nTransaction Hash:\n'+strtx),
                            reply_markup=transdone())
                        except:
                            context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\nThere seems to be a problem with your network connection, please try again later'),
                            reply_markup=balmenu())
                else:
                    context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.005037 BNB'),
                    reply_markup=balmenu())
            else:
                context.bot.send_message(chat_id = chat_id, text = ("You don't seem to have enough TTK in your account. Each user is required to have at least 200,000 TTk before transactions can work"),
                reply_markup=balmenu())

        else:
            context.bot.send_message(chat_id = chat_id, text = 'No transfer in progress')

    elif last_command == "create-busd":
        amount = float(update.message.text)* 1
        shareamount = int(amount)
        client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"last_command": "busd-share"}}))
        update.message.reply_text(username+' How many users would you like to share this rain '+person)

    elif last_command == "busd-share":
        people = int(update.message.text)
        peeps=str(people)
        approveamount = 1000**10
        gas_required = int(337000000000000)
        bnb_balance = int(w3.eth.get_balance(Owner))
        tokens_left=str(busdcontract.functions.balanceOf(rain_address).call()/10**18)
        client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"last_command": ""}}))
        if bnb_balance > gas_required:
            try:
                w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
                w3.eth.default_account = Owner
                busdcontract.functions.approve(rain_address, approveamount).transact({'from': w3.eth.defaultAccount})
                raincontract.functions.createRain(shareamount, people, busd_address).transact({'from': w3.eth.defaultAccount})
                person = int(shareamount/people)
                perperson = str(person)
                context.bot.send_message(chat_id = chat_id, text = ('CREATION SUCCESSFUL\n\nThis rain was created for '+peeps+' users each user will get '+perperson+' BUSD when they claim'),
                reply_markup=balmenu())
            except:
                context.bot.send_message(chat_id = chat_id, text = ('CREATION FAILED\n\nYou do not meet the requirements\n1.Your Wallet BUSD balance must be up to the amount you want to share\n2.The last BUSD token rain must be over (Rain stops when all tokens are claimed or removed)\nTokens left to claim: '+tokens_left+' BUSD'),
                reply_markup=balmenu())
        else:
            context.bot.send_message(chat_id = chat_id, text = ('CREATION FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.000337 BNB'),
            reply_markup=balmenu())

    elif last_command == "create-usdt":
        amount = float(update.message.text)* 1
        shareamount = int(amount)
        client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"last_command": "usdt-share"}}))
        update.message.reply_text(username+' How many users would you like to share this rain')

    elif last_command == "usdt-share":
        people = int(update.message.text)
        peeps=str(people)
        approveamount = 1000**10
        gas_required = int(337000000000000)
        bnb_balance = int(w3.eth.get_balance(Owner))
        tokens_left=str(usdtcontract.functions.balanceOf(rain_address).call()/10**18)
        client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"last_command": ""}}))
        if bnb_balance > gas_required:
            try:
                w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
                w3.eth.default_account = Owner
                usdtcontract.functions.approve(rain_address, approveamount).transact({'from': w3.eth.defaultAccount})
                raincontract.functions.createRain(shareamount, people, usdt_address).transact({'from': w3.eth.defaultAccount})
                person = int(shareamount/people)
                perperson = str(person)
                context.bot.send_message(chat_id = chat_id, text = ('CREATION SUCCESSFUL\n\nThis rain was created for '+peeps+' users each user will get '+perperson+' BUSD when they claim'),
                reply_markup=balmenu())
            except:
                context.bot.send_message(chat_id = chat_id, text = ('CREATION FAILED\n\nYou do not meet the requirements\n1.Your Wallet USDT balance must be up to the amount you want to share\n2.The last USDT token rain must be over (Rain stops when all tokens are claimed or removed)\nTokens left to claim: '+tokens_left+' USDT'),
                reply_markup=balmenu())
        else:
            context.bot.send_message(chat_id = chat_id, text = ('CREATION FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.000337 BNB'),
            reply_markup=balmenu())

    elif last_command == "create-ttk":
        amount = float(update.message.text)* 1
        shareamount = int(amount)
        client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"last_command": "ttk-share"}}))
        update.message.reply_text(username+' How many users would you like to share this rain')

    elif last_command == "ttk-share":
        people = int(update.message.text)
        peeps=str(people)
        approveamount = 1000**10
        gas_required = int(337000000000000)
        bnb_balance = int(w3.eth.get_balance(Owner))
        tokens_left=str(ttkcontract.functions.balanceOf(rain_address).call()/10**18)
        client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"last_command": ""}}))
        if bnb_balance > gas_required:
            try:
                w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
                w3.eth.default_account = Owner
                ttkcontract.functions.approve(rain_address, approveamount).transact({'from': w3.eth.defaultAccount})
                raincontract.functions.createRain(shareamount, people, ttk_address).transact({'from': w3.eth.defaultAccount})
                person = int(shareamount/people)
                perperson = str(person)
                context.bot.send_message(chat_id = chat_id, text = ('CREATION SUCCESSFUL\n\nThis rain was created for '+peeps+' users  each user will get '+perperson+' TTK when they claim'),
                reply_markup=balmenu())
            except:
                context.bot.send_message(chat_id = chat_id, text = ('CREATION FAILED\n\nYou do not meet the requirements\n1.Your Wallet TTK balance must be up to the amount you want to share\n2.The last TTK token rain must be over (Rain stops when all tokens are claimed or removed)\nTokens left to claim: '+tokens_left+' TTK'),
                reply_markup=balmenu())
        else:
            context.bot.send_message(chat_id = chat_id, text = ('CREATION FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.000337 BNB'),
            reply_markup=balmenu())
    else:
        if chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
            y = 1 + 1
        else:
            update.message.reply_text(message+'??,'+username+' I do not understand what that means, please try saying something else')

def error(update, context):
    print(f'The main error be sey {context.error}')

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

############################ Keyboards #########################################
def main_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Account', callback_data='m1')],
              [InlineKeyboardButton('Finances', callback_data='m2')],
              [InlineKeyboardButton('See Prices', callback_data='Prices')],
              [InlineKeyboardButton('Contact Us', callback_data='Contact')]]
  return InlineKeyboardMarkup(keyboard)
def first_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Sign up', callback_data='Signup')],
                [InlineKeyboardButton('View Private Key', callback_data='ViewKey')],
                [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)
def second_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Balance', callback_data='balance')],
                [InlineKeyboardButton('Deposit', callback_data='Deposit'),
                InlineKeyboardButton('Transfer', callback_data='Transfer')],
                [InlineKeyboardButton('Rain', callback_data='Rain'),
                InlineKeyboardButton('Swap (Coming Soon)', callback_data='ksi')],
                [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)
def back_to_main():
    keyboard = [[InlineKeyboardButton('Go Back', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)
def go_to_depo():
    keyboard = [[
                InlineKeyboardButton(text='BNB', callback_data='Depaddress'),
                InlineKeyboardButton('BEP20 TOKENS', callback_data='Depaddress'),
                ],
                [InlineKeyboardButton('TTK', callback_data='Depaddress'),
                ],
                [InlineKeyboardButton('Go Back', callback_data='m2'),]]
    return InlineKeyboardMarkup(keyboard)
def go_to_trans():
    keyboard = [[
                InlineKeyboardButton(text='BNB', callback_data='Bngive'),
                InlineKeyboardButton(text='BUSD', callback_data='Bsgive'),
                InlineKeyboardButton(text='USDT', callback_data='Usgive'),
                ],
                [InlineKeyboardButton('TTK', callback_data='Give')],
                [InlineKeyboardButton('Go Back', callback_data='m2'),]]
    return InlineKeyboardMarkup(keyboard)
def go_to_rain():
    keyboard = [[InlineKeyboardButton(text='Create Rain', callback_data='CreateRain')],
                [InlineKeyboardButton(text='Claim Rain', callback_data='ClaimRain')],
                [InlineKeyboardButton('Stop Rain', callback_data='StopRain')],
                [InlineKeyboardButton('Go Back', callback_data='m2'),]]
    return InlineKeyboardMarkup(keyboard)
def makerain():
    keyboard = [[
                InlineKeyboardButton(text='BUSD', callback_data='Busdrain'),
                InlineKeyboardButton(text='USDT', callback_data='Usdtrain'),
                ],
                [InlineKeyboardButton('TTK', callback_data='Ttkrain')],
                [InlineKeyboardButton('Go Back', callback_data='m2'),]]
    return InlineKeyboardMarkup(keyboard)
def Claimrain():
    keyboard = [[
                InlineKeyboardButton(text='BUSD', callback_data='Busdclaim'),
                InlineKeyboardButton(text='USDT', callback_data='Usdtclaim'),
                ],
                [InlineKeyboardButton('TTK', callback_data='Ttkclaim')],
                [InlineKeyboardButton('Go Back', callback_data='m2'),]]
    return InlineKeyboardMarkup(keyboard)
def Endrain():
    keyboard = [[
                InlineKeyboardButton(text='BUSD', callback_data='Busdstop'),
                InlineKeyboardButton(text='USDT', callback_data='Usdtstop'),
                ],
                [InlineKeyboardButton('TTK', callback_data='Ttkstop')],
                [InlineKeyboardButton('Go Back', callback_data='m2'),]]
    return InlineKeyboardMarkup(keyboard)
def signed():
    keyboard = [[InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)
def transdone():
    keyboard = [[InlineKeyboardButton(text='Veiw Transaction', url=hash_link)],
                [InlineKeyboardButton('Go Back', callback_data='m2'),
                InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)
def balmenu():
    keyboard = [[InlineKeyboardButton('Go Back', callback_data='m2'),
                InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)
########################## Account Redirectors #################################

def Signup(update, context):
    global KEY
    global Owner
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("name"), chat_id)))
    # admin = client.query(q.get(q.match(q.index("Admindata"), adminnumber)))
    using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
    password = using["data"]["password"]
    KEY = secrets.token_hex(14)
    # totalreg = admin["data"]["totalregistered"]
    account = w3.eth.account.create('uwefwe2920r2jj303jr20rr09r4')
    address = str(account.address)
    key = HexBytes.hex(account.key)
    if password == "":
        Owner = address
        # totalsigned = totalreg + 1
        client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"logged_in": "dids"}}))
        client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"signed_up": "natrue"}}))
        client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"password": KEY}}))
        client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"address": address}}))
        client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"private-key": key}}))
        # client.query(q.update(q.ref(q.collection("UserUpdates"), adminnumber), {"data": {"totalusers": totalsigned}}))
        # client.query(q.update(q.ref(q.collection("UserUpdates"), adminnumber), {"data": {"Latestusername": username}}))
        # client.query(q.update(q.ref(q.collection("UserUpdates"), adminnumber), {"data": {"latestuseraddress": address}}))
        context.bot.send_message(chat_id = chat_id, text =('Sign Up Successful\n\nYour new Deposit Address:\n'+address+'\n\n You now have full access to the BSC Telegram BOT powered by TTK '),
                                reply_markup=signed())
        # context.bot.send_message(chat_id = eben_id, text =('Hi Admin\nA new user has just signed up with these details\nFirst Name: '+first_name+'\nLastname: '+last_name+'\nAddress:\n'+address+'\nNOTE: If any entry is left blank this user did not register their telegram account with that field'))
        # context.bot.send_message(chat_id = doc_id, text =('Hi Admin\nA new user has just signed up with these details\nFirst Name: '+first_name+'\nLastname: '+last_name+'\nAddress:\n'+address+'\nNOTE: If any entry is left blank this user did not register their telegram account with that field'))
    else:
        context.bot.send_message(chat_id = chat_id, text =(username+' You have already signed up for this service'),
                                reply_markup=signed())

def ViewKey(update, context):
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("name"), chat_id)))
    using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
    password = using["data"]["password"]
    Owner = using["data"]["address"]
    keys = using["data"]["private-key"]
    allowance = int(200000*10**18)
    try:
        username=using["data"]["username"]
    except:
        username = ''
    if password == "":
        context.bot.send_message(chat_id = chat_id, text =(username+' You cannot view your accounts private key without signing up without signing up'),
        reply_markup=first_menu_keyboard())
    else:
        ttkbalance = int(ttkcontract.functions.balanceOf(Owner).call())
        if ttkbalance < allowance:
            context.bot.send_message(chat_id = chat_id, text =(username+' Your TTK balance must be above 200,000 before you have access to your account private key'))
        elif ttkbalance > allowance:
            context.bot.send_message(chat_id = chat_id, text =(username+' Your BSC BOT private key is:\n'+keys))
        else:
            context.bot.send_message(chat_id = chat_id, text =(username+' There seems to br a problem with your connection please try again later'))
############################# Messages #########################################
def main_menu_message():
  return 'What would you like to do today:'

def first_menu_message():
  return 'Setup your Wallet'

def second_menu_message():
  return 'What would you like to do with your finances today:'
def Contact(bot, update):
    bot.callback_query.message.edit_text(('Want to make a complaint?, Or request for addition of your custom token?, Contact us at info@ttk.finance or visit our website '+website),
    reply_markup=back_to_main())
def Prices(update, context):
    chat_id = update.effective_chat.id
    bnbpage = requests.get('https://coinmarketcap.com/currencies/binance-coin/')
    btcpage = requests.get('https://www.coindesk.com/price/bitcoin')
    ethpage = requests.get('https://www.coindesk.com/price/ethereum')
    bnbtree = html.fromstring(bnbpage.content)
    btctree = html.fromstring(btcpage.content)
    ethtree = html.fromstring(ethpage.content)
    _bnbprice = str(bnbtree.xpath('//div[@class="priceValue___11gHJ "]/text()'))
    _btcprice = str(btctree.xpath('//div[@class="price-large"]/text()'))
    _ethprice = str(ethtree.xpath('//div[@class="price-large"]/text()'))
    bnb_price = _bnbprice.strip(" [''] ")
    btc_price = _btcprice.strip(" [''] ")
    eth_price = _ethprice.strip(" [''] ")
    context.bot.send_message(chat_id = chat_id, text =('Right now the prices are:\n'+btc_price+' per BTC\n'+eth_price+' per ETH\n'+bnb_price+' per BNB'),
    reply_markup=back_to_main())

############################# Finanace Handers ####################################
def Transfer(update, context):
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("name"), chat_id)))
    using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
    password = using["data"]["password"]
    try:
        username=using["data"]["username"]
    except:
        username = ''
    if password == "":
        context.bot.send_message(chat_id = chat_id, text =(username+' You cannot make a transfer without signing up'),
        reply_markup=first_menu_keyboard())
    else:
        context.bot.send_message(chat_id = chat_id, text =('What currency would you like to transfer'),
        reply_markup=go_to_trans())

def Give(update, context):
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("name"), chat_id)))
    client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"last_command": "address"}}))
    client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"transfer-type": "ttk"}}))
    context.bot.send_message(chat_id = chat_id, text = 'What address would you like to send some TTK to:')

def Bngive(update, context):
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("name"), chat_id)))
    client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"last_command": "address"}}))
    client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"transfer-type": "bnb"}}))
    context.bot.send_message(chat_id = chat_id, text = 'Please enter the address you want BNB transfered to:')

def Bsgive(update, context):
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("name"), chat_id)))
    client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"last_command": "address"}}))
    client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"transfer-type": "busd"}}))
    context.bot.send_message(chat_id = chat_id, text = 'What address are you transfering BUSD to:')

def Usgive(update, context):
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("name"), chat_id)))
    client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"last_command": "address"}}))
    client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"transfer-type": "usdt"}}))
    context.bot.send_message(chat_id = chat_id, text = 'What address will you be transfering USDT to:')


def Deposit(update, context):
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("name"), chat_id)))
    using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
    password = using["data"]["password"]
    if password == "":
        context.bot.send_message(chat_id=chat_id, text = (username+' You cannot see your deposit address without Signing up'),
                                reply_markup=first_menu_keyboard())
    else:
        context.bot.send_message(chat_id = chat_id, text =('What Currency would you like to deposit?'),
        reply_markup=go_to_depo())

def Depaddress(update, context):
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("name"), chat_id)))
    address = user["data"]["address"]
    try:
        using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
        username=using["data"]["username"]
    except:
        username = ''
    context.bot.send_message(chat_id = chat_id, text = ('Hi '+username+'\nYour Deposit Address:\n'+address+'\nNOTE:\nThis address can only recieve TTK, BNB, BUSD and USDT(BEP20)'),
    reply_markup=balmenu())

def balance(update, context):
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("name"), chat_id)))
    using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
    address = using["data"]["address"]
    signed = using["data"]["signed_up"]
    try:
        using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
        username=using["data"]["username"]
    except:
        username = ''
    if signed == "":
        context.bot.send_message(chat_id = chat_id, text = (username+' You have not signed up for this service'),
        reply_markup=balmenu())
    else:
        ttk_balance = str(ttkcontract.functions.balanceOf(address).call()/10**18)
        bnb_bal = str(w3.eth.get_balance(address)/10**18)
        busd_bal = str(busdcontract.functions.balanceOf(address).call()/10**18)
        usdt_bal = str(usdtcontract.functions.balanceOf(address).call()/10**18)
        context.bot.send_message(chat_id = chat_id, text = ('Your Account Balance today is: \n'+ttk_balance+' TTK,\n'+bnb_bal+' BNB,\n'+busd_bal+' BUSD,\n'+usdt_bal+' USDT'),
        reply_markup=balmenu())

################################## Rain ########################################

def Rain(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id = chat_id, text = ('You can share tokens equally to user using our TTK wallet Rain'),
    reply_markup=go_to_rain())

def CreateRain(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id = chat_id, text = ('What token would you like to create a rain for:'),
    reply_markup=makerain())

def Busdrain(update, context):
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("name"), chat_id)))
    client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"last_command": "create-busd"}}))
    context.bot.send_message(chat_id = chat_id, text = ('How many BUSD would you like to share'),
    reply_markup=balmenu())

def Usdtrain(update, context):
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("name"), chat_id)))
    client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"last_command": "create-usdt"}}))
    context.bot.send_message(chat_id = chat_id, text = ('How many USDT would you like to share'),
    reply_markup=balmenu())

def Ttkrain(update, context):
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("name"), chat_id)))
    client.query(q.update(q.ref(q.collection("Login-details"), user["ref"].id()), {"data": {"last_command": "create-ttk"}}))
    context.bot.send_message(chat_id = chat_id, text = ('How many TTK would you like to share'),
    reply_markup=balmenu())

def ClaimRain(update, context):
    chat_id = update.effective_chat.id
    ttk_left=str(ttkcontract.functions.balanceOf(rain_address).call()/10**18)
    busd_left=str(busdcontract.functions.balanceOf(rain_address).call()/10**18)
    usdt_left=str(usdtcontract.functions.balanceOf(rain_address).call()/10**18)
    context.bot.send_message(chat_id = chat_id, text = ('What token would you like to claim\n\n'+ttk_left+'TTK left to claim\n'+busd_left+'BUSD left to claim\n'+usdt_left+'USDT left to claim'),
    reply_markup=Claimrain())

def Busdclaim(update, context):
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("name"), chat_id)))
    using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
    Owner = using["data"]["address"]
    private_key = using["data"]["private-key"]
    gas_required = int(337000000000000)
    bnb_balance = int(w3.eth.get_balance(Owner))
    tokens_left=str(busdcontract.functions.balanceOf(rain_address).call()/10**18)
    if bnb_balance > gas_required:
        try:
            w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
            w3.eth.default_account = Owner
            tx_hash = raincontract.functions.claimRain(busd_address).transact({'from': w3.eth.defaultAccount})
            context.bot.send_message(chat_id = chat_id, text = ('BUSD CLAIM SUCCESSFUL\n\n Your claim has been added to your account, and you cannot claim twice'),
            reply_markup=balmenu())
        except:
            context.bot.send_message(chat_id = chat_id, text = ('BUSD CLAIM FAILED\n\nYou did not meet the requirements\n1.Each user can only claim once\n2.Rain must have tokens left to claim (Rain stops when all tokens are removed)\nTokens left to claim: '+tokens_left+' BUSD'),
            reply_markup=balmenu())
    else:
        context.bot.send_message(chat_id = chat_id, text = ('CLAIM FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.000337 BNB'),
        reply_markup=balmenu())

def Usdtclaim(update, context):
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("name"), chat_id)))
    using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
    Owner = using["data"]["address"]
    private_key = using["data"]["private-key"]
    gas_required = int(337000000000000)
    bnb_balance = int(w3.eth.get_balance(Owner))
    tokens_left=str(usdtcontract.functions.balanceOf(rain_address).call()/10**18)
    if bnb_balance > gas_required:
        try:
            w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
            w3.eth.default_account = Owner
            tx_hash = raincontract.functions.claimRain(usdt_address).transact({'from': w3.eth.defaultAccount})
            context.bot.send_message(chat_id = chat_id, text = ('USDT CLAIM SUCCESSFUL\n\n Your claim has been added to your account, and you cannot claim twice'),
            reply_markup=balmenu())
        except:
            context.bot.send_message(chat_id = chat_id, text = ('USDT CLAIM FAILED\n\nYou did not meet the requirements\n1.Each user can only claim once\n2.Rain must have tokens left to claim (Rain stops when all tokens are removed)\nTokens left to claim: '+tokens_left+' USDT'),
            reply_markup=balmenu())
    else:
        context.bot.send_message(chat_id = chat_id, text = ('CLAIM FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.000337 BNB'),
        reply_markup=balmenu())

def Ttkclaim(update, context):
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("name"), chat_id)))
    using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
    Owner = using["data"]["address"]
    private_key = using["data"]["private-key"]
    gas_required = int(337000000000000)
    bnb_balance = int(w3.eth.get_balance(Owner))
    tokens_left=str(ttkcontract.functions.balanceOf(rain_address).call()/10**18)
    if bnb_balance > gas_required:
        try:
            w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
            w3.eth.default_account = Owner
            tx_hash = raincontract.functions.claimRain(ttk_address).transact({'from': w3.eth.defaultAccount})
            context.bot.send_message(chat_id = chat_id, text = ('TTK CLAIM SUCCESSFUL\n\n Your claim has been added to your account, and you cannot claim twice'),
            reply_markup=balmenu())
        except:
            context.bot.send_message(chat_id = chat_id, text = ('TTK CLAIM FAILED\n\nYou did not meet the requirements\n1.Each user can only claim once\n2.Rain must have tokens left to claim (Rain stops when all tokens are removed)\nTokens left to claim: '+tokens_left+' TTK'),
            reply_markup=balmenu())
    else:
        context.bot.send_message(chat_id = chat_id, text = ('CLAIM FAILED\n\nYour Balance is insufficient for this transaction\nGas fee required is 0.000337 BNB'),
        reply_markup=balmenu())



def StopRain(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id = chat_id, text = ('What token would you like to stop:'),
    reply_markup=Endrain())

def Busdstop(update, context):
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("name"), chat_id)))
    using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
    Owner = using["data"]["address"]
    private_key = using["data"]["private-key"]
    tokens_left=str(busdcontract.functions.balanceOf(rain_address).call()/10**18)
    try:
        w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
        w3.eth.default_account = Owner
        tx_hash = raincontract.functions.TakeRain(busd_address).transact({'from': w3.eth.defaultAccount})
        context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION SUCCESSFUL\n\n Tokens left have been returned to your account'),
        reply_markup=balmenu())
    except:
        context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\n\nYou did not meet the requirements\n1.You must be the Rain creator\n2.Rain must have tokens left to remove (Rain stops automatically when all tokens are removed)\nTokens left to claim: '+tokens_left+' BUSD'),
        reply_markup=balmenu())

def Usdtstop(update, context):
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("name"), chat_id)))
    using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
    Owner = using["data"]["address"]
    private_key = using["data"]["private-key"]
    tokens_left=str(usdtcontract.functions.balanceOf(rain_address).call()/10**18)
    try:
        w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
        w3.eth.default_account = Owner
        tx_hash = raincontract.functions.TakeRain(usdt_address).transact({'from': w3.eth.defaultAccount})
        context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION SUCCESSFUL\n\n Tokens left have been returned to your account'),
        reply_markup=balmenu())
    except:
        context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\n\nYou did not meet the requirements\n1.You must be the Rain creator\n2.Rain must have tokens left to remove (Rain stops automatically when all tokens are removed)\nTokens left to claim: '+tokens_left+'USDT'),
        reply_markup=balmenu())

def Ttkstop(update, context):
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("name"), chat_id)))
    using = client.query(q.get(q.ref(q.collection("Login-details"), user["ref"].id())))
    Owner = using["data"]["address"]
    private_key = using["data"]["private-key"]
    tokens_left=str(ttkcontract.functions.balanceOf(rain_address).call()/10**18)
    try:
        w3.middleware_onion.add(construct_sign_and_send_raw_middleware(private_key))
        w3.eth.default_account = Owner
        tx_hash = raincontract.functions.TakeRain(ttk_address).transact({'from': w3.eth.defaultAccount})
        context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION SUCCESSFUL\n\n Tokens left have been returned to your account'),
        reply_markup=balmenu())
    except:
        context.bot.send_message(chat_id = chat_id, text = ('TRANSACTION FAILED\n\nYou did not meet the requirements\n1.You must be the Rain creator\n2.Rain must have tokens left to remove (Rain stops automatically when all tokens are removed)\nTokens left to claim: '+tokens_left+' TTK'),
        reply_markup=balmenu())

############################# Handlers #########################################
client = FaunaClient(secret=fauna_secret)


updater = Updater(TOKEN, use_context="natrue")

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('transfer', oddtransfer))
updater.dispatcher.add_handler(CommandHandler('deposit', deposit))
updater.dispatcher.add_handler(CommandHandler('balance', balance))
updater.dispatcher.add_handler(CommandHandler('rain', rain))
updater.dispatcher.add_handler(CommandHandler('price', Prices))

unknown_handler = MessageHandler(Filters.command, unknown)
########################## Callback Handlers ###################################
updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
updater.dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
updater.dispatcher.add_handler(CallbackQueryHandler(Contact, pattern='Contact'))
updater.dispatcher.add_handler(CallbackQueryHandler(Prices, pattern='Prices'))
updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu, pattern='m1_1'))
updater.dispatcher.add_handler(CallbackQueryHandler(second_submenu, pattern='m2_1'))
updater.dispatcher.add_handler(CallbackQueryHandler(Deposit, pattern='Deposit'))
updater.dispatcher.add_handler(CallbackQueryHandler(Depaddress, pattern='Depaddress'))
updater.dispatcher.add_handler(CallbackQueryHandler(Transfer, pattern='Transfer'))
updater.dispatcher.add_handler(CallbackQueryHandler(Give, pattern='Give'))
updater.dispatcher.add_handler(CallbackQueryHandler(Bngive, pattern='Bngive'))
updater.dispatcher.add_handler(CallbackQueryHandler(Bsgive, pattern='Bsgive'))
updater.dispatcher.add_handler(CallbackQueryHandler(Usgive, pattern='Usgive'))
updater.dispatcher.add_handler(CallbackQueryHandler(balance, pattern='balance'))
updater.dispatcher.add_handler(CallbackQueryHandler(Rain, pattern='Rain'))
updater.dispatcher.add_handler(CallbackQueryHandler(CreateRain, pattern='CreateRain'))
updater.dispatcher.add_handler(CallbackQueryHandler(ClaimRain, pattern='ClaimRain'))
updater.dispatcher.add_handler(CallbackQueryHandler(StopRain, pattern='StopRain'))
updater.dispatcher.add_handler(CallbackQueryHandler(Busdrain, pattern='Busdrain'))
updater.dispatcher.add_handler(CallbackQueryHandler(Usdtrain, pattern='Usdtrain'))
updater.dispatcher.add_handler(CallbackQueryHandler(Ttkrain, pattern='Ttkrain'))
updater.dispatcher.add_handler(CallbackQueryHandler(Busdclaim, pattern='Busdclaim'))
updater.dispatcher.add_handler(CallbackQueryHandler(Ttkclaim, pattern='Ttkclaim'))
updater.dispatcher.add_handler(CallbackQueryHandler(Usdtclaim, pattern='Usdtclaim'))
updater.dispatcher.add_handler(CallbackQueryHandler(Busdstop, pattern='Busdstop'))
updater.dispatcher.add_handler(CallbackQueryHandler(Usdtstop, pattern='Usdtstop'))
updater.dispatcher.add_handler(CallbackQueryHandler(Ttkstop, pattern='Ttkstop'))
updater.dispatcher.add_handler(CallbackQueryHandler(Signup, pattern='Signup'))
updater.dispatcher.add_handler(CallbackQueryHandler(ViewKey, pattern='ViewKey'))

updater.dispatcher.add_error_handler(error)
updater.dispatcher.add_handler(unknown_handler)
# Get the dispatcher to register handlers
dp = updater.dispatcher

# on noncommand i.e message - echo the message on Telegram
dp.add_handler(MessageHandler(Filters.text, echo))

# Start the Bot
updater.start_polling()

# Run the bot until you press Ctrl-C and will stop the bot gracefully.
updater.idle()
################################################################################
