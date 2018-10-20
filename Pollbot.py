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
from Poll import *
from threading import Thread
from time import sleep
from RocketchatBot import RocketChatBot
from emojistorage import *

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('[%(asctime)s %(levelname)s] %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class PollBot(RocketChatBot):

    def __init__(self, botname, password, server):
        super().__init__(botname,password,server)
        self.polls = dict()
        self.msg_to_poll = dict()
        self.commands.append((['poll', ], self.poll))

    def check_poll_messages(self):
        deleted_messages = []
        for msg,poll in self.msg_to_poll.items():
            logger.info("Checking Poll %s" % msg)
            try:
                message = self.api.chat_get_message(msg_id=msg).json()
                creation_msg = self.api.chat_get_message(msg_id=poll.creation_msg).json()
                if not creation_msg['success']:
                    self.api.chat_delete(room_id=message['message']['rid'], msg_id=poll.poll_msg)
                    deleted_messages.append(msg)
                    return
                elif message['message']['reactions'] != poll.reactions:
                    logger.info("REACTIONS CHANGED FOR MESSAGE:\n %s" % message)
                    poll.reactions = message['message']['reactions']
                    poll.process_reactions(self.botname)
                    updated_message,attachments = poll.create_message()
                    self.api.chat_update(room_id=message['message']['rid'], msg_id=poll.poll_msg,text=updated_message, attachments=attachments)
            except Exception as err:
                logger.warning(err)
                deleted_messages.append(msg)
        for msg in deleted_messages:
            self.msg_to_poll.pop(msg, None)

    def run(self):
        for channel in self.api.channels_list_joined().json().get('channels'):
            self.load_channel_ts(channel.get('_id'))

        while 1:
            for channel in self.api.channels_list_joined().json().get('channels'):
                Thread(target=self.process_channel, args=(channel.get('_id'),)).start()
                Thread(target=self.check_poll_messages).start()
            sleep(1)

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
        return poll

    def poll(self, msg_id, args, user, channel_id):
        args = [z.strip() for z in args.strip().split('"')]
        args = list(filter(None, args))
        self.create_poll(channel_id, args, msg_id)
