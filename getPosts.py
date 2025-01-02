from misskey import Misskey
import json
from os import path

users = []
updateNotes = False

if path.isfile("./allnotes.json"):
    updateNotes = True
    currentNotes = json.load(open("./allnotes.json"))
    for user in currentNotes:
        users.append([user["userId"], user["instance"], user["token"], user["notes"][0]["id"]])
else:
    currentNotes = []
    usersFile = open("users.csv").read().split("\n")[:-1]
    for line in usersFile:
        if len(line) == 0: continue
        users.append(line.replace(" ", "").split(",") + [None])

for user in users:
    print("Found user id {} on instance {} with token {}".format(user[0], user[1], user[2]))

output = []

def getNotes(userId, instance, token, since = None):
    mk = Misskey(instance, i=token)
    print("Using token {}".format(token))
    print("Getting notes for user {} on instance {}...".format(userId, instance))
    if updateNotes:
        print("Updating notes...")
        notes = mk.users_notes(user_id = userId, limit = 100, include_replies = True, include_my_renotes = False, since_id = since)
        allNotes = notes
        isComplete = False
        noteCount = len(notes)
        print("Got {} notes".format(noteCount))
        if noteCount != 100: isComplete = True
        while not isComplete:
            print("Got {} notes".format(noteCount))
            notes = mk.users_notes(user_id = userId, limit = 100, include_replies = True, since_id = notes[0]["id"], include_my_renotes = False)
            allNotes = notes + allNotes
            noteCount = noteCount + len(notes)
            if len(notes) != 100: isComplete = True
        allNotes.reverse()
        return allNotes
    notes = mk.users_notes(user_id = userId, limit = 100, include_replies = True, include_my_renotes = False)
    allNotes = notes
    isComplete = False
    noteCount = len(notes)
    if noteCount == 0: isComplete = True
    while not isComplete:
        print("Got {} notes".format(noteCount))
        notes = mk.users_notes(user_id = userId, limit = 100, include_replies = True, until_id = notes[-1]["id"], include_my_renotes = False)
        allNotes = allNotes + notes
        noteCount = noteCount + len(notes)
        if len(notes) != 100: isComplete = True

    print("Got {} notes".format(noteCount))
    print("done with user {}".format(userId))
    return allNotes

for user in users:
    output.append({"userId": user[0], "instance": user[1], "token": user[2], "notes": getNotes(user[0], user[1], user[2], user[3])})

if updateNotes:
    for user in range(len(currentNotes)):
        if output[user]["notes"] == []:
            print("Skipping user as no new notes were recieved")
            continue
        else:
            currentNotes[user]["notes"] = output[user]["notes"] + currentNotes[user]["notes"]
else:
    currentNotes = output

json.dump(currentNotes, open("./allnotes.json", 'w'), indent="  ")
