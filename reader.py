"""Personal, read-only Reddit reader for hardware hobby research.
Fetches this week's top posts (and their top comments) from a few
hardware subreddits using application-only OAuth. No posting, voting,
messaging or any other write action. Under 500 requests/day.
"""
import os
import time
import requests

SUBS = ["cyberDeck", "hardwarehacking", "SBCs", "retrogaming", "homelab"]
UA = "script:alex-hw-reader:0.1 (by /u/akex7987)"


def get_token():
    r = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=(os.environ["REDDIT_CLIENT_ID"], os.environ["REDDIT_CLIENT_SECRET"]),
        data={"grant_type": "client_credentials"},
        headers={"User-Agent": UA},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["access_token"]


def get(path, token, **params):
    r = requests.get(
        "https://oauth.reddit.com" + path,
        headers={"Authorization": "bearer " + token, "User-Agent": UA},
        params=params,
        timeout=30,
    )
    r.raise_for_status()
    time.sleep(2)
    return r.json()


def main():
    token = get_token()
    for sub in SUBS:
        top = get("/r/%s/top" % sub, token, t="week", limit=10)
        for child in top["data"]["children"]:
            p = child["data"]
            print("[%s] %s (%d) https://reddit.com%s" % (sub, p["title"], p["score"], p["permalink"]))
            comments = get("/comments/%s" % p["id"], token, limit=5, depth=1)
            for c in comments[1]["data"]["children"][:5]:
                body = c["data"].get("body", "").replace("\n", " ")[:200]
                if body:
                    print("    - " + body)


if __name__ == "__main__":
    main()
