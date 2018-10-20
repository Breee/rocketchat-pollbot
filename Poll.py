"""
MIT License

Copyright (c) 2018 Breee@github

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


from emojistorage import *
import time


class PollCreationException(Exception):
    pass

POLL_ID = 0

class Poll(object):
    """
    A Poll object, used as parent for SinglePoll and MultiPoll.
    """

    def __init__(self, poll_title, vote_options):
        global POLL_ID
        self.poll_ID = POLL_ID
        POLL_ID += 1
        self.creation_time = time.time() # timestamp
        self.poll_msg = None
        self.creation_msg = None
        self.creator = None

        self.poll_title = poll_title # string

        # vote_options of the form [op1,op2,op3...]
        self.vote_options = vote_options

        # reactions dict is of the form:
        # {':regional_indicator_a:': {'usernames': ['testbot', 'Bree']},
        #  ':regional_indicator_b:': {'usernames': ['testbot']},
        #  ':regional_indicator_c:': {'usernames': ['testbot']}}
        self.reactions = dict()
        self.options_to_users = dict()
        self.user_to_amount = dict()
        self.option_to_reaction = dict()
        self.reaction_to_option = dict()

        for i, option in enumerate(vote_options):
            if i in EmojiStorage.NUMBER_TO_LETTEREMOJI:
                reaction = EmojiStorage.NUMBER_TO_LETTEREMOJI[i]
                self.option_to_reaction[option] = reaction
                self.reaction_to_option[reaction] = option
                self.options_to_users[option] = []

    def process_reactions(self, botname):
        tmp = {key: [] for key in self.options_to_users}
        self.options_to_users = tmp
        self.user_to_amount = dict()
        for reaction, userdict in self.reactions.items():
            users = userdict['usernames']
            if reaction in EmojiStorage.LETTEREMOJI_TO_NUMBER:
                option = self.reaction_to_option[reaction]
                for user in users:
                    if user != botname:
                        if user not in self.user_to_amount:
                            self.user_to_amount[user] = 1
                        self.options_to_users[option].append(user)
            elif reaction in EmojiStorage.DEFAULT_PEOPLE_EMOJI_TO_NUMBER:
                for user in users:
                    if user != botname:
                        if user not in self.user_to_amount:
                            self.user_to_amount[user] = EmojiStorage.DEFAULT_PEOPLE_EMOJI_TO_NUMBER[reaction]
                        else:
                            self.user_to_amount[user] += EmojiStorage.DEFAULT_PEOPLE_EMOJI_TO_NUMBER[reaction]


    def create_message(self):
        """
        creates message of the form:

        TITLE

        Reaction1 Option1 [5]
        user1 [2], user2 [3]

        Reaction2 Option2 [2]
        user3[1], user4[1]

        :return:
        """

        attachments = {"title": self.poll_title, "color": "#ff6644", 'collapsed': False}
        msg = "*%s* \n" % (self.poll_title)
        text = ""
        for option, users in self.options_to_users.items():
            reaction = self.option_to_reaction[option]
            user_string = ""
            total = 0
            for i in range(len(users)):
                user = users[i]
                amount = self.user_to_amount[user]
                user_string += "%s [%d]" % (user, amount)
                total += amount
                if i < len(users)-1:
                    user_string += ", "

            msg += "*%s %s [%d]* \n %s \n " % (reaction, option,total,user_string)
            text += "*%s %s [%d]* \n %s \n " % (reaction, option,total,user_string)

        attachments['text'] = text
        return msg, [attachments]
