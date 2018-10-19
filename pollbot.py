"""
MIT License

Copyright (c) Breee@github 2018
Copyright (c) 2017 Jorge Alberto Díaz Orozco (Akiel) (diazorozcoj@gmail.com)



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
from Poll import *
from random import choice
from threading import Thread
from time import sleep
from rocketchat_API.rocketchat import RocketChat
from config import *


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('[%(asctime)s %(levelname)s] %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class RocketChatBot(object):
    def __init__(self, botname, passwd, server):
        self.botname = botname
        self.api = RocketChat(botname, passwd, server, ssl_verify=False)
        self.commands = [(['echo', ], self.echo)]
        self.auto_answers = []
        self.direct_answers = []
        self.unknow_command = ['command not found', ]
        self.lastts = {}
        self.polls = dict()
        self.msg_to_poll = dict()
        self.add_dm_handler(['poll'], self.poll)

    def echo(self, msg, user, channel_id):
        self.send_message('@' + user + ' : ' + msg, channel_id)

    def get_status(self, user):
        return self.api.users_get_presence(username=user)

    def send_message(self, msg, channel_id,attachments=None):
        return self.api.chat_post_message(channel=channel_id, text=msg,
                                          attachments=attachments)

    def add_dm_handler(self, command, action):
        self.commands.append((command, action))

    def add_auto_answer(self, triggers, answers):
        self.auto_answers.append((triggers, answers))

    def add_direct_answer(self, triggers, answers):
        self.direct_answers.append((triggers, answers))

    def handle_direct_message(self, message, channel_id):
        msg = message['msg'].lstrip('@' + self.botname).strip()
        if len(msg) > 0:
            command = msg.split()[0].lower()
            arguments = " ".join(msg.split()[1:])
            user = message['u']['username']
            for cmd_list in self.commands:
                if command.lower() in cmd_list[0]:
                    cmd_list[1](arguments, user, channel_id)
                    return

            if not self.handle_auto_answer(message, self.direct_answers, channel_id):
                self.send_message('@' + user + ' :' + choice(self.unknow_command), channel_id)
        else:
            self.send_message('Here I am', channel_id)

    def handle_auto_answer(self, message, answers, channel_id):
        for kind in answers:
            for k in kind[0]:
                if k in message['msg'].lower():
                    self.send_message(choice(kind[1]) + ' @' + message['u']['username'], channel_id)
                    return True
        return False

    def handle_messages(self, messages, channel_id):
        for message in messages['messages']:
            if message['u']['username'] != self.botname:
                logger.info(message)
                if message['u']['username'] == 'rocket.cat':
                    continue
                if message['msg'].startswith('@' + self.botname):
                    Thread(target=self.handle_direct_message, args=(message, channel_id)).start()
                elif 'mentions' not in message or message.get('mentions') == []:
                    Thread(target=self.handle_auto_answer, args=(message, self.auto_answers, channel_id)).start()

    def load_ts(self, channel_id, messages):
        if len(messages) > 0:
            self.lastts[channel_id] = messages[0]['ts']
        else:
            self.lastts[channel_id] = ''

    def load_channel_ts(self, channel_id):
        self.load_ts(channel_id, self.api.channels_history(channel_id).json()['messages'])

    def load_group_ts(self, channel_id):
        self.load_ts(channel_id, self.api.groups_history(channel_id).json()['messages'])

    def load_im_ts(self, channel_id):
        response = self.api.im_history(channel_id).json()
        if response.get('success'):
            self.load_ts(channel_id, self.api.im_history(channel_id).json()['messages'])

    def process_messages(self, messages, channel_id):
        try:
            if len(messages['messages']) > 0:
                self.lastts[channel_id] = messages['messages'][0]['ts']
            self.handle_messages(messages, channel_id)
        except Exception as e:
            logger.info(e)

    def process_channel(self, channel_id):
        if channel_id not in self.lastts:
            self.lastts[channel_id] = ''

        self.process_messages(self.api.channels_history(channel_id, oldest=self.lastts[channel_id]).json(),
                              channel_id)

    def process_group(self, channel_id):
        if channel_id not in self.lastts:
            self.lastts[channel_id] = ''

        self.process_messages(self.api.groups_history(channel_id, oldest=self.lastts[channel_id]).json(),
                              channel_id)

    def process_im(self, channel_id):
        if channel_id not in self.lastts:
            self.lastts[channel_id] = ''

        self.process_messages(self.api.im_hdistory(channel_id, oldest=self.lastts[channel_id]).json(),
                              channel_id)

    def check_poll_messages(self):
        for msg,poll in self.msg_to_poll.items():
            logger.info("[+] Checking Poll %s" % msg)
            message = bot.api.chat_get_message(msg_id=msg).json()
            if message['message']['reactions'] != poll.reactions:
                logger.info(message)
                poll.reactions = message['message']['reactions']
                poll.process_reactions(self.botname)
                updated_message,attachments = poll.create_message()
                self.api.chat_update(room_id=message['message']['rid'],msg_id=poll.poll_msg,text=updated_message, attachments=attachments)


    def run(self):
        for channel in self.api.channels_list_joined().json().get('channels'):
            self.load_channel_ts(channel.get('_id'))

        while 1:
            for channel in self.api.channels_list_joined().json().get('channels'):
                Thread(target=self.process_channel, args=(channel.get('_id'),)).start()
                Thread(target=self.check_poll_messages).start()
            sleep(1)

    def create_poll(self, channel_id, poll_args):
        if len(poll_args) < 2:
            usage = "Error, usage: @botname poll <poll_title> <option_1> .. <option_10>"
            self.send_message(msg=usage, channel_id=channel_id)
            return
        title = poll_args[0]
        vote_options = poll_args[1:]
        poll = Poll(poll_title=title, vote_options=vote_options)
        message,attachments = poll.create_message()
        callback = self.send_message(msg=message, channel_id=channel_id,attachments=None).json()
        poll.poll_msg = callback['message']['_id']
        for reaction, option in poll.reaction_to_option.items():
            self.api.chat_react(msg_id=poll.poll_msg, emoji=reaction)
        self.msg_to_poll[poll.poll_msg] = poll
        return poll

    def poll(self, msg, user, channel_id):
        args = msg.strip().split(' ')
        poll = self.create_poll(channel_id, args)


botname = BOTNAME
botpassword = PASSWORD
server_url = SERVER
bot = RocketChatBot(botname, botpassword, server_url)
bot.run()
