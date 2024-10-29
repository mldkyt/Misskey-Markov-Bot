from misskey import Misskey
import generate
import json
from os import path

if not path.isfile("./allnotes.json"):
    print("No notes found! Please fetch posts first then try again.")
    quit()

# Get the token from the token file
token = json.load(open("./allnotes.json"))[0]["token"]
instance = json.load(open("./allnotes.json"))[0]["instance"]

# Read the generated post
post = generate.generatePost()
print("Posting:", post, sep="\n")

mk = Misskey(instance, i=token)

mk.notes_create(
    text = post,
    visibility = "home",
    cw = "markov generated post"
)
