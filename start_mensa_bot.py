from Mensabot import MensaBot
from config import *

botname = BOTNAME
botpassword = PASSWORD
server_url = SERVER
bot = MensaBot(botname, botpassword, server_url)
bot.run()
