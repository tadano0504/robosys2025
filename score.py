#!/usr/bin/env python3
# SPDX-FileCopyrightTest: 2025 Keito Tadano
# SPDX-License-Identifier: GPL-3.0-only

import requests
import sys

API_KEY = "ここに自分のAPIキー"
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

    if not matches:
        return None

    # 新しい順
    matches = sorted(matches, key=lambda x: x["utcDate"], reverse=True)

    # ① FINISHED を優先
    for m in matches:
        if m["status"] in ["FINISHED", "AWARDED"]:
            return m

    # ② なければ最新試合
    return matches[0]


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
    home = ENGLISH_NAMES.get(match["homeTeam"]["name"], match["homeTeam"]["name"])
    away = ENGLISH_NAMES.get(match["awayTeam"]["name"], match["awayTeam"]["name"])

    score = match["score"]["fullTime"]
    h = score.get("home", 0)
    a = score.get("away", 0)

    status = match["status"]

    if status not in ["FINISHED", "AWARDED"]:
        # LIVE / IN_PLAY / TIMED など
        result = status
    else:
        # FINISHED のときだけ勝敗判定
        if h > a:
            result = "WIN"
        elif h < a:
            result = "LOSE"
            pass
        else:
            result = "DRAW"

    # 相手チーム名を表示
    opponent = away if home == team["name_en"] else home

    print(date)
    print(opponent)
    print(f"{result} {h}-{a}")


if __name__ == "__main__":
    main()

