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
import copy
from Poll import *
from threading import Thread
from time import sleep
from RocketchatBot import RocketChatBot
from emojistorage import *
from utils import replace_quotes
import shlex
import pickle
import os

logger = logging.getLogger('bot')


class PollBot(RocketChatBot):

    def __init__(self, botname, password, server):
        super().__init__(botname,password,server)
        self.polls = dict()
        self.msg_to_poll = dict()
        self.commands.append((['poll', ], self.poll))
        self.commands.append((['help', ], self.help))
        self.dump_file = 'msg_to_poll.pickle'
        logger.info("load stored polls")
        if os.path.isfile(self.dump_file):
            msg_to_poll = pickle.load(file=open(self.dump_file, 'rb'))
            self.msg_to_poll = msg_to_poll
        logger.info("done.")

    def check_poll_messages(self, messages):
        messages = messages.json()
        print(len(messages['messages']))
        deleted_messages = []
        copy_msg_to_poll = self.msg_to_poll.copy()
        for msg in messages['messages'][0:100]:
            id = msg['_id']
            if id in copy_msg_to_poll:
                poll = copy_msg_to_poll[id]
                if msg['reactions'] != poll.reactions:
                    poll.reactions = self.preprocess_reactions(msg['reactions'])
                    poll.process_reactions(self.botname)
                    updated_message, attachments = poll.create_message()
                    self.api.chat_update(room_id=msg['rid'], msg_id=poll.poll_msg, text=updated_message,
                                         attachments=attachments)
        for msg in deleted_messages:
            self.msg_to_poll.pop(msg, None)

    def preprocess_reactions(self, reactions):
        """
        Function to replace usernames (e.g. @bree) in reactions with the name set in rocketchat(e.g. bree123).
        """
        reactions_copy = copy.deepcopy(reactions)
        for reaction, userdict in reactions.items():
            users = userdict['usernames']
            for user in users:
                if user != self.botname:
                    userinfo = self.api.users_info(username=user).json()
                    user_name = userinfo['user']['name']
                    if user != user_name:
                        if user in reactions_copy[reaction]['usernames']:
                            reactions_copy[reaction]['usernames'].remove(user)
                            reactions_copy[reaction]['usernames'].append(user_name)
        return reactions_copy

    def process_messages(self, messages, channel_id):
        try:
            if len(messages['messages']) > 0:
                self.lastts[channel_id] = messages['messages'][0]['ts']
            self.handle_messages(messages, channel_id)
            msgs = self.api.channels_history(channel_id, count=1000)
            self.check_poll_messages(messages=msgs)
        except Exception as e:
            logger.info(e)

    def run(self):
        for channel in self.api.channels_list_joined().json().get('channels'):
            self.load_channel_ts(channel.get('_id'))

        while 1:
            for channel in self.api.channels_list_joined().json().get('channels'):
                Thread(target=self.process_channel, args=(channel.get('_id'),)).start()
                #self.process_channel(channel.get('_id'))
            sleep(3)

    def create_poll(self, channel_id, poll_args, msg_id):
        logger.info("Creating new poll with arguments %s"  % poll_args)
        if len(poll_args) < 2:
            usage = "Error, usage: @botname poll <poll_title> <option_1> .. <option_10>"
            self.send_message(msg=usage, channel_id=channel_id)
            logger.info("Not enough arguments provided, aborting poll creation.")
            return
        title = poll_args[0]
        vote_options = poll_args[1:]
        poll = Poll(poll_title=title, vote_options=vote_options)
        poll.creation_msg = msg_id
        message,attachments = poll.create_message()
        callback = self.send_message(msg=message, channel_id=channel_id,attachments=None).json()
        poll.poll_msg = callback['message']['_id']
        # add reaction for each vote_option.
        for reaction, option in poll.reaction_to_option.items():
            self.api.chat_react(msg_id=poll.poll_msg, emoji=reaction)
        # add +1,+2,+3,+4
        for reaction in EmojiStorage.DEFAULT_PEOPLE_EMOJI_TO_NUMBER.keys():
            self.api.chat_react(msg_id=poll.poll_msg, emoji=reaction)

        self.msg_to_poll[poll.poll_msg] = poll
        pickle.dump(self.msg_to_poll,file=open(self.dump_file,'wb'))
        return poll

    def poll(self, msg_id, args, user, channel_id):
        args = replace_quotes(args)
        args = shlex.split(args)
        args = list(filter(None, args))
        self.create_poll(channel_id, args, msg_id)

    def help(self, msg_id, args, user, channel_id):
        usage = "Usage: `@botname poll <poll_title> <option_1> .. <option_10>`\n" \
                "For example: `@botname poll mensa 11:30 11:45 12:00`"
        self.send_message(msg=usage, channel_id=channel_id)
