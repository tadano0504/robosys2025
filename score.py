#!/home/keito/anaconda3/bin/python3
# SPDX-FileCopyrightTest: 2025 Keito Tadano
# SPDX-License-Identifier: GPL-3.0-only

import requests
import sys

API_KEY = "2c4165142758434abcfab08ee6203d49"
BASE = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}

ENGLISH_NAMES = {
    "Athletic Club": "Athletic Bilbao",
    "Club Atlético de Madrid": "Atletico Madrid",
    "CA Osasuna": "Osasuna",
    "RCD Espanyol de Barcelona": "Espanyol",
    "FC Barcelona": "Barcelona",
    "Getafe CF": "Getafe",
    "Real Madrid CF": "Real Madrid",
    "Rayo Vallecano de Madrid": "Rayo Vallecano",
    "Levante UD": "Levante",
    "RCD Mallorca": "Mallorca",
    "Real Betis Balompié": "Real Betis",
    "Real Sociedad de Fútbol": "Real Sociedad",
    "Villarreal CF": "Villarreal",
    "Valencia CF": "Valencia",
    "Deportivo Alavés": "Alaves",
    "Elche CF": "Elche",
    "Girona FC": "Girona",
    "RC Celta de Vigo": "Celta Vigo",
    "Sevilla FC": "Sevilla",
    "Real Oviedo": "Real Oviedo"
}


def load_laliga_teams():
    url = f"{BASE}/competitions/PD/teams"
    r = requests.get(url, headers=HEADERS)
    data = r.json()
    teams = data.get("teams", [])
    result = {}
    for t in teams:
        es = t["name"]
        en = ENGLISH_NAMES.get(es, es)
        result[en.lower()] = {"id": t["id"], "name_en": en}
    return result


def get_latest_finished_match(team_id):
    url = f"{BASE}/teams/{team_id}/matches?limit=50"
    r = requests.get(url, headers=HEADERS)
    matches = r.json().get("matches", [])
    matches = sorted(matches, key=lambda x: x["utcDate"], reverse=True)
    for m in matches:
        if m["status"] == "FINISHED":
            return m
    return None


def main():
    if len(sys.argv) < 2:
        print("使い方: score.py <チーム名>")
        sys.exit(1)

    input_name = " ".join(sys.argv[1:]).lower()
    teams = load_laliga_teams()

    if input_name not in teams:
        print("入力したチーム名が見つかりません。以下の中から正しい英語名を入力してください：")
        for name in sorted(teams.keys()):
            print(teams[name]["name_en"])
        return

    team = teams[input_name]
    match = get_latest_finished_match(team["id"])

    if not match:
        print("データがありません")
        return

    date = match["utcDate"]
    home = match["homeTeam"]["name"]
    away = match["awayTeam"]["name"]

    home = ENGLISH_NAMES.get(home, home)
    away = ENGLISH_NAMES.get(away, away)

    score = match["score"]["fullTime"]
    h, a = score["home"], score["away"]

    if home.lower() == team["name_en"].lower():
        team_score = h
        opp_score = a
    else:
        team_score = a
        opp_score = h

    if team_score > opp_score:
        result = "WIN"
    elif team_score < opp_score:
        result = "LOSE"
    else:
        result = "DRAW"

    print(date)
    print(away if home == team["name_en"] else home)
    print(f"{result} {h}-{a}")


if __name__ == "__main__":
    main()

