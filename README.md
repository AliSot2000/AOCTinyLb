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

Help Message:
```bash
usage: main.py [-h] [-c COOKIE] [-u URL] [-U USERS] [-a ADD] [-r REMOVE]

Small Webcrawler for JellyTabby to see what the friends are doing in AOC

optional arguments:
  -h, --help            show this help message and exit
  -c COOKIE, --cookie COOKIE
                        Google Authentication cookie from JellyTabby
  -u URL, --url URL     URL JellyTabby wants to pull the Data from
  -U USERS, --users USERS
                        Output file for the JSON data, i.e. "['USERNAME']"
  -a ADD, --add ADD     Add a user to the list
  -r REMOVE, --remove REMOVE
                        Remove a user from the list

```
