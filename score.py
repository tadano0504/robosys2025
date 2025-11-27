#!/usr/bin/env python3
import requests
import sys

API_KEY = "2c4165142758434abcfab08ee6203d49"

BASE = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}

def get_team_id(name):
    url = f"{BASE}/competitions/PD/teams"
    r = requests.get(url, headers=HEADERS)
    data = r.json()

    teams = data.get("teams", [])

    for t in teams:
        if t["name"].lower() == name.lower():
            return t["id"]

    for t in teams:
        if name.lower() in t["name"].lower():
            return t["id"]

    return None

def get_latest_match(team_id):
    url = f"{BASE}/teams/{team_id}/matches?limit=50"
    r = requests.get(url, headers=HEADERS)
    data = r.json()

    matches = data.get("matches", [])
    if not matches:
        return None

    matches = sorted(matches, key=lambda m: m["utcDate"], reverse=True)

    for m in matches:
        if m["status"] == "FINISHED":
            return m

    return matches[0]

def main():
    if len(sys.argv) < 2:
        print("usage: score.py <team name>")
        sys.exit(1)

    team_name = " ".join(sys.argv[1:])
    team_id = get_team_id(team_name)
    if team_id is None:
        print("no data")
        return

    match = get_latest_match(team_id)
    if not match:
        print("no data")
        return

    date = match["utcDate"]
    home = match["homeTeam"]["name"]
    away = match["awayTeam"]["name"]
    score = match.get("score", {}).get("fullTime")

    print(date)

    if home.lower() == team_name.lower():
        opponent = away
        my_score = score["home"]
        opp_score = score["away"]
    else:
        opponent = home
        my_score = score["away"]
        opp_score = score["home"]

    print(opponent)

    if my_score > opp_score:
        result = "WIN"
    elif my_score < opp_score:
        result = "LOSE"
    else:
        result = "DRAW"

    print(f"{result} {my_score}-{opp_score}")

if __name__ == "__main__":
    main()

