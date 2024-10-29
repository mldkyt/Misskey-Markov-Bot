import markovify
import re
import json
from os import path

def formatPost(inFile, filterFile=None):
    text = []
    notes = json.load(open(inFile))
    filterList = []
    containsFilteredWord = False
    if filterFile != None:
        with open(filterFile) as f:
            filterList = [s.strip() for s in f.read().split(',')]
    for user in notes:
        for note in user["notes"]:
            if note["text"] == None: continue
            if note["visibility"] == "specified" or note["visibility"] == "followers": continue
            if note["cw"] == "#miceco": continue
            for word in filterList:
                if (note["cw"] != None and word in note["cw"]):
                    containsFilteredWord = True
                    continue
                elif word in note["text"]:
                    containsFilteredWord = True
                else:
                    containsFilteredWord = False
            if containsFilteredWord: continue
            text.append(note["text"].replace("\n", "\\n"))
    return text

def generatePost():
    text = formatPost("./allnotes.json") if not path.isfile("./filter.csv") else formatPost("./allnotes.json", "./filter.csv")
    text_model = markovify.NewlineText(text, well_formed=False)
    post = text_model.make_sentence(tries=100)
    post = re.sub(r'^@', "@​", post)
    post = re.sub(r'\s@', " @​", post)
    post = post.replace('\\n', '\n')
    return post
