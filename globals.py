from config.config import Config
from loguru import logger
from aiogram import Bot
from db_models.User import engine
from aiogram import Dispatcher
from sites import Bomber

#-_-_-_-_-_-CONNECTS-_-_-_-_-_-#
try:
    config = Config() #Config load
    logger.info("[+] True loaded configuration")
except Exception as e:
    logger.exception(e)

try:
    bot = Bot(token = config.token, parse_mode="html") #connect t0 Telegram API
    dp:Dispatcher = None
    logger.info("[+] True connect to Telegram API")
except Exception as e:
    logger.exception(e)

engine.connect()

#-_-_-_-_-_-VARIABLES -_-_-_-_-_-#
username_bot:str = None #Username bot
data_numbers_kv:dict = None #All public numbers

seconds:int = 0      #Counter variable
start_attack:Bomber = None
now_process:bool = True #Process T/F
attack_country:str = None

mail_button = None
mail_content:str = None
mail_count:int = 0

state_data:list = []

#-_-_-_-_-_-KEYBOARDS-_-_-_-_-_-#
ru_keyboards:list = [
    ["👤Мой профиль"], 
    ["💣Атаковать номер"],
    ["🌐Изменить язык"],
    ["📲Купить виртуальный номер"]
]

eng_keyboards:list = [
    ["👤My profile"], 
    ["💣Attack number"], 
    ["🌐Change the language"]
]