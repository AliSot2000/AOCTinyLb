# AOCTinyLb
The Advent of Code Tiny Leaderboard
Given an Advent of Code Leader Board, an authentication cookie from google, and a list of usernames, this small scraper allows you to only display a select number of users so you don't have so sifth through the entire leader board to compare yourself aginst your friends.

Initial usage:
To run the script initially, the command should look something like this:
```bash
python3 main.py -c "<cookie copied from request header of a request>" -u "<url to AOC leaderboard>" -U '["USERNAME1", "USERNAME2"]'
```

All this is going to be stored in a local config file .config.json
If the cookie should become invalid at some point, just add a new cookie with -c

The script allows you to add users with `-a` or `--add` and then a username or a JSON list of users `'["USERNAME1", "USERNAME2"]'`
You can also remove users with `-r` or `--remove` and then a username of a JSON list of users `'["USERNAME1", "USERNAME2"]'`

Have fun with the script.
