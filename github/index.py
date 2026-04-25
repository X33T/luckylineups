import random
from flask import Flask, request, jsonify

app = Flask(__name__)


def get_player_pool(style: str) -> list:
    if style == "batting":
        return list(range(1, 6)) * 4 + list(range(6, 12)) * 1
    elif style == "bowling":
        return list(range(1, 6)) * 1 + list(range(6, 12)) * 4
    else:
        return list(range(1, 12))


def pick_numbers(style: str, count: int) -> list:
    pool = get_player_pool(style)
    chosen = []
    while len(chosen) < count:
        pick = random.choice(pool)
        if pick not in chosen:
            chosen.append(pick)
    return sorted(chosen)


def generate_teams(team_a: str, team_b: str, style: str, num_teams: int) -> list:
    results = []
    used_combos = set()

    for i in range(1, num_teams + 1):
        attempts = 0
        while attempts < 50:
            n_a = random.choice([5, 6])
            n_b = 11 - n_a

            players_a = pick_numbers(style, n_a)
            players_b = pick_numbers(style, n_b)

            all_players = (
                [(team_a, n) for n in players_a] +
                [(team_b, n) for n in players_b]
            )

            if style == "batting":
                preferred = [p for p in all_players if p[1] <= 5]
            elif style == "bowling":
                preferred = [p for p in all_players if p[1] >= 6]
            else:
                preferred = all_players

            cap_pool = preferred if len(preferred) >= 2 else all_players
            captain  = random.choice(cap_pool)
            vc_pool  = [p for p in cap_pool if p != captain]
            vice_cap = random.choice(vc_pool)

            combo_key = (captain, vice_cap)
            if combo_key not in used_combos:
                used_combos.add(combo_key)
                break
            attempts += 1

        results.append({
            "index":        i,
            "team_a":       {"name": team_a, "players": players_a},
            "team_b":       {"name": team_b, "players": players_b},
            "captain":      {"team": captain[0],  "number": captain[1]},
            "vice_captain": {"team": vice_cap[0], "number": vice_cap[1]},
        })

    return results


@app.route("/generate", methods=["POST"])
def generate():
    data      = request.json
    team_a    = data.get("team_a", "Team A").strip()
    team_b    = data.get("team_b", "Team B").strip()
    style     = data.get("style", "balanced").lower()
    num_teams = int(data.get("num_teams", 1))

    if style not in ("batting", "bowling", "balanced"):
        return jsonify({"error": "Invalid style"}), 400
    if num_teams < 1:
        return jsonify({"error": "num_teams must be at least 1"}), 400

    teams = generate_teams(team_a, team_b, style, num_teams)
    return jsonify({"teams": teams, "style": style})
