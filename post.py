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
from os import path

from misskey import Misskey

import generate

if __name__ == '__main__':
    if not path.isfile("./allnotes.json"):
        print("No notes found! Please fetch posts first then try again.")
        quit()

    # Get the token from the token file
    token = json.load(open("./allnotes.json"))[0]["token"]
    instance = json.load(open("./allnotes.json"))[0]["instance"]

    # Read the generated post
    post = generate.generate_post()
    print("Posting:", post, sep="\n")

    mk = Misskey(instance, i=token)

    mk.notes_create(
        text=post,
        visibility="home",
        cw="markov generated post"
    )
