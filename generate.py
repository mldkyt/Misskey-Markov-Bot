#       Misskey-Markov-Bot
#       Copyright (C) 2024  ChloeCat
#
#       This program is free software: you can redistribute it and/or modify it under the
#       terms of the GNU Affero General Public License as published by the Free Software
#       Foundation, either version 3 of the License, or (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful, but WITHOUT ANY
#       WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
#       PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.
#
#       You should have received a copy of the GNU Affero General Public License along
#       with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import json
import re
from os import path

import markovify


def format_post(in_file, filter_file=None):
    text = []
    notes = json.load(open(in_file))
    filter_list = []
    contains_filtered_word = False
    if filter_file is not None:
        with open(filter_file) as f:
            filter_list = [s.strip() for s in f.read().split(',')]
    for user in notes:
        for note in user["notes"]:
            if note["text"] is None: continue
            if note["visibility"] == "specified" or note["visibility"] == "followers": continue
            if note["cw"] == "#miceco": continue
            for word in filter_list:
                if note["cw"] is not None and word in note["cw"]:
                    contains_filtered_word = True
                    continue
                elif word in note["text"]:
                    contains_filtered_word = True
                else:
                    contains_filtered_word = False
            if contains_filtered_word: continue
            text.append(note["text"].replace("\n", "\\n"))
    return text


def generate_post():
    text = format_post("./allnotes.json") if not path.isfile("./filter.csv") else format_post("./allnotes.json",
                                                                                              "./filter.csv")
    text_model = markovify.NewlineText(text, well_formed=False)
    post = text_model.make_sentence(tries=100)
    post = re.sub(r'^@', "@​", post)
    post = re.sub(r'\s@', " @​", post)
    post = post.replace('\\n', '\n')
    return post
