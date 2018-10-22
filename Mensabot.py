"""
MIT License

Copyright (c) Breee@github 2018

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import logging
from Pollbot import PollBot
import urllib.request, json
from config import MENSA_CACHE_URL, MENSA_NAMES, DEFAULT_MENSA

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('[%(asctime)s %(levelname)s] %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class MensaBot(PollBot):

    def __init__(self, botname, password, server):
        super().__init__(botname,password,server)
        self.commands.append((['food', 'essen'], self.food))


    def food(self, msg_id, args, user, channel_id):

        if not args:
            args = DEFAULT_MENSA

        with urllib.request.urlopen(MENSA_CACHE_URL) as url:
            data = json.loads(url.read().decode())

        usage = "Usage: `@BOTNAME [food | essen] %s`" % MENSA_NAMES
        if not args:
            self.send_message(msg=usage, channel_id=channel_id)
        else:
            mensa = args.strip().replace('ß', 'ss')
            food = data[mensa]
            foodmsg = ""
            for day, dishes in food.items():
                if dishes[0]['bezeichnung'] == 'heute keine Essensausgabe':
                    continue
                foodmsg += "*%s*:\n" % day
                for dish in dishes:
                        foodmsg += "* %s: %s\n" % (dish['bezeichnung'], dish['gericht'].replace('<br>', ', '))
                foodmsg += "\n"

            self.send_message(msg=foodmsg, channel_id=channel_id)

