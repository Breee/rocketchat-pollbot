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

class EmojiStorage(object):

    def __init__(self):
        # Dictionary that maps the numblock emojis to a number.
        self.EMOJI_TO_NUMBER = {
            "\U00000031\U000020E3": 0,
            "\U00000032\U000020E3": 1,
            "\U00000033\U000020E3": 2,
            "\U00000034\U000020E3": 3,
            "\U00000035\U000020E3": 4,
            "\U00000036\U000020E3": 5,
            "\U00000037\U000020E3": 6,
            "\U00000038\U000020E3": 7,
            "\U00000039\U000020E3": 8,
            "\U0001F51F": 9
            }

        # Reverse of EMOJI_TO_NUMBER
        self.NUMBER_TO_EMOJI = {val: key for key, val in self.EMOJI_TO_NUMBER.items()}

        """
        :regional_indicator_a:  \U0001F1E6
        :regional_indicator_b:  \U0001F1E7
        :regional_indicator_c:  \U0001F1E8
        :regional_indicator_d:  \U0001F1E9
        :regional_indicator_e: \U0001F1EA
        :regional_indicator_f: \U0001F1EB
        :regional_indicator_g:  \U0001F1EC
        :regional_indicator_h:  \U0001F1ED
        :regional_indicator_i:  \U0001F1EE
        :regional_indicator_j:  \U0001F1EF
        """

        self.LETTEREMOJI_TO_NUMBER = {
            ':regional_indicator_a:': 0,
            ':regional_indicator_b:': 1,
            ':regional_indicator_c:': 2,
            ':regional_indicator_d:': 3,
            ':regional_indicator_e:': 4,
            ':regional_indicator_f:': 5,
            ':regional_indicator_g:': 6,
            ':regional_indicator_h:': 7,
            ':regional_indicator_i:': 8,
            ':regional_indicator_j:': 9
            }

        self.NUMBER_TO_LETTEREMOJI = {val: key for key, val in self.LETTEREMOJI_TO_NUMBER.items()}

        # Dictionary that maps the people emojis to a number.
        # The emojis in this dict are used in the raid-poll to express the amount of extra people someone
        #  brings to a raid.

        self.DEFAULT_PEOPLE_EMOJI_TO_NUMBER = {
            ":plus_one:": 1,
            ":plus_two:": 2,
            ":plus_three:": 3,
            ":plus_four:": 4
            }


    def is_people_emoji(self, emoji):
        return emoji in self.DEFAULT_PEOPLE_EMOJI_TO_NUMBER.keys()

    def get_people_emoji_value(self,emoji):
        if emoji in self.DEFAULT_PEOPLE_EMOJI_TO_NUMBER.keys():
            return self.DEFAULT_PEOPLE_EMOJI_TO_NUMBER[emoji]


EmojiStorage = EmojiStorage()
