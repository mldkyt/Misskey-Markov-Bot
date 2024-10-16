# Misskey-Markov-Bot

A markov bot for misskey.

# Requirements

This script requires the [`Misskey.py`](https://pypi.org/project/Misskey.py/) and [`Markovify`](https://pypi.org/project/markovify/) python libraries.

# Usage

To start, create a file called `users.csv`. This is where all the information about which users to uses as a corpus. The format of the file is as follows:
```
<user id>, <instance url>, <api key>
<user id>, <instance url>, <api key>
...
```

The api token and instance that is listed will be the one used to post the generated notes.

`user id` should be the id of the user that you wish the bot to follow. This must be the id from the instance that the `instance url` and `api key` are from. This is set up to allow multiple users on different instances to be followed *from their own instance*, in order to allow for more complete coverage.

Once that file is set up, run `getposts.py` to retrive the posts from the specified users. This will output a file called `allnotes.json`, which will be used by the other scripts to create the markov posts.

Finally, run `post.py` to create the post. It will post to the instance and api key that is specified first in the `users.csv` file.

## Future updates

I plan on eventually adding a filter list, to remove notes that contain unwanted words from the corpus.
