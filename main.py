import json
import argparse
import os
from dataclasses import dataclass

import requests


@dataclass
class Config:
    cookie_dict = {}
    url = ""
    users = []

    def to_dict(self):
        return {
            "cookies": self.cookie_dict,
            "url": self.url,
            "users": self.users
        }


@dataclass
class User:
    username: str = ""
    id = ""
    score = 0
    stars = 0


def compare(a: User, b: User) -> int:
    return a.score > b.score


def fill(base: str, length: int, fill_char: str = " "):
    if len(base) >= length:
        return base

    return base + fill_char * (length - len(base))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Small Webcrawler for JellyTabby to see what the friends are doing in AOC')
    parser.add_argument('-c', '--cookie', help='Google Authentication cookie from JellyTabby', type=str, default=None)
    parser.add_argument('-u', '--url', help='URL JellyTabby wants to pull the Data from', type=str, default=None)
    parser.add_argument('-U', '--users', help='Output file for the JSON data, i.e. \"[\'USERNAME\']\"', type=str, default=None)
    parser.add_argument('-a', '--add', help='Add a user to the list', type=str, default=None)
    parser.add_argument('-r', '--remove', help='Remove a user from the list', type=str, default=None)
    arguments = parser.parse_args()

    cfg = Config()

    worked = True
    changed = False

    path = os.path.join(os.path.dirname(__file__), ".config.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            config = json.load(f)

            config: dict
            if "cookies" in config.keys() and type(config["cookies"]) == str:
                cfg.cookie_dict = config["cookies"]
            else:
                worked = False

            if "url" in config.keys() and type(config["url"]) == str:
                cfg.url = config["url"]
            else:
                worked = False

            if "users" in config.keys() and type(config["users"]) == list:
                cfg.users = config["users"]
            else:
                worked = False

            if not worked:
                print("Error: Config file is not valid, new config will be generated with full command")

    else:
        worked = False

    if not worked:
        print("Your config file is not valid or doesn't exist, please enter the following information")
        print("Users, Cookies, URL")

        if arguments.cookie is None or arguments.url is None or arguments.users is None:
            print("Error: Cookies, Users and url are required to generate a config")
            exit(1)

        cfg.cookie_dict = arguments.cookie
        cfg.url = arguments.url
        cfg.users = json.loads(arguments.users)
        changed = True

    if (arguments.users is not None) and (arguments.add is not None or arguments.remove is not None):
        print("Cannot provice both a user list and add/remove users")
        exit(1)

    if (arguments.add is not None) and worked:
        try:
            user_list = json.loads(arguments.add)
            cfg.users.extend(json.loads(arguments.add))

        except json.JSONDecodeError:
            cfg.users.append(arguments.add)

        changed = True

    if (arguments.remove is not None) and worked:
        try:
            remove_users = json.loads(arguments.remove)
        except json.JSONDecodeError:
            remove_users = [arguments.remove]

        for user in remove_users:
            if user in cfg.users:
                cfg.users.remove(user)
                changed = True
            else:
                print(f"User {user} was not in list")

    if changed:
        with open(path, "w") as f:
            json.dump(cfg.to_dict(), f, indent="  ")

    resp = requests.get(cfg.url, headers={"user-agent": "JellyTabby WebCrawler", "cookie": cfg.cookie_dict})

    if not resp.ok:
        print(f"Failed to query AOC with Status Code: {resp.status_code}\n{resp.text}")
        exit(1)

    data = resp.json()
    all_users = []

    # create a datastructure in python to store the data
    for key, value in data["members"].items():
        user = User()
        user.username = value["name"]
        user.id = key
        user.score = value["local_score"]

        # compute the stars
        for _, day, in value["completion_day_level"].items():
            user.stars += len(day.keys())

        all_users.append(user)

    all_users.sort(key=lambda x: x.score, reverse=True)

    header = fill("Rank", 4) + " | " + fill("Score", 6) + " | " + fill("Stars", 5) + " | " + "Username"  #f"{'Username':<20}{'Score':>10}{'Stars':>10}"
    print(header)
    print("-" * (len(header) + 20))

    for i in range(len(all_users)):
        u = all_users[i]
        if u.username in cfg.users:
            user_string = fill(str(i), 4) + " | " + fill(str(u.score), 6) + " | " + fill(str(u.stars), 5) + " | " + u.username
            print(user_string)

