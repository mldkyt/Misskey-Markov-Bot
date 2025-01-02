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


def get_notes(user_id, instance, token, since=None):
    mk = Misskey(instance, i=token)
    print("Using token {}".format(token))
    print("Getting notes for user {} on instance {}...".format(user_id, instance))
    if update_notes:
        print("Updating notes...")
        notes = mk.users_notes(user_id=user_id, limit=100, include_replies=True, include_my_renotes=False,
                               since_id=since)
        all_notes = notes
        is_complete = False
        note_count = len(notes)
        print("Got {} notes".format(note_count))
        if note_count != 100: is_complete = True
        while not is_complete:
            print("Got {} notes".format(note_count))
            notes = mk.users_notes(user_id=user_id, limit=100, include_replies=True, since_id=notes[0]["id"],
                                   include_my_renotes=False)
            all_notes = notes + all_notes
            note_count = note_count + len(notes)
            if len(notes) != 100: is_complete = True
        all_notes.reverse()
        return all_notes
    notes = mk.users_notes(user_id=user_id, limit=100, include_replies=True, include_my_renotes=False)
    all_notes = notes
    is_complete = False
    note_count = len(notes)
    if note_count == 0: is_complete = True
    while not is_complete:
        print("Got {} notes".format(note_count))
        notes = mk.users_notes(user_id=user_id, limit=100, include_replies=True, until_id=notes[-1]["id"],
                               include_my_renotes=False)
        all_notes = all_notes + notes
        note_count = note_count + len(notes)
        if len(notes) != 100: is_complete = True

    print("Got {} notes".format(note_count))
    print("done with user {}".format(user_id))
    return all_notes


if __name__ == '__main__':
    users = []
    update_notes = False

    if path.isfile("./allnotes.json"):
        update_notes = True
        with open('./allnotes.json', 'r', encoding='utf8') as f:
            current_notes = json.load(f)
        for user in current_notes:
            users.append([user["userId"], user["instance"], user["token"], user["notes"][0]["id"]])
    else:
        current_notes = []
        usersFile = open("users.csv").read().split("\n")[:-1]
        for line in usersFile:
            if len(line) == 0: continue
            users.append(line.replace(" ", "").split(",") + [None])

    for user in users:
        print("Found user id {} on instance {} with token {}".format(user[0], user[1], user[2]))

    output = []

    for user in users:
        output.append({"userId": user[0], "instance": user[1], "token": user[2],
                       "notes": get_notes(user[0], user[1], user[2], user[3])})

    if update_notes:
        for user in range(len(current_notes)):
            if not output[user]["notes"]:
                print("Skipping user as no new notes were recieved")
                continue
            else:
                current_notes[user]["notes"] = output[user]["notes"] + current_notes[user]["notes"]
    else:
        current_notes = output

    with open("./allnotes.json", 'w', encoding='utf8') as f:
        json.dump(current_notes, f, indent="  ")
