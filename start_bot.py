from Pollbot import PollBot
from config import *

botname = BOTNAME
botpassword = PASSWORD
server_url = SERVER
bot = PollBot(botname, botpassword, server_url)
bot.run()
