import markovify
import re
import json

def formatPost(inFile):
    text = []
    notes = json.load(open(inFile))
    for user in notes:
        for note in user["notes"]:
            if note["text"] == None: continue
            if note["visibility"] == "specified" or note["visibility"] == "followers": continue
            if note["cw"] == "#miceco": continue
            text.append(note["text"].replace("\n", "\\n"))
    return text

def generatePost():
    text = formatPost("./allnotes.json")
    text_model = markovify.NewlineText(text, well_formed=False)
    post = text_model.make_sentence(tries=100)
    post = re.sub(r'^@', "@​", post)
    post = re.sub(r'\s@', " @​", post)
    post = post.replace('\\n', '\n')
    return post
