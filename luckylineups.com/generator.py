import random

# Role mapping
BATTERS = list(range(1, 6))     # 1–5
ALL_ROUNDERS = [6, 7]           # 6–7
BOWLERS = list(range(8, 13))    # 8–12


def pick_team(mode="random"):
    team_a = []
    team_b = []

    def build_set(size, bowlers_needed):
        team = []

        # Pick bowlers
        bowlers = random.sample(BOWLERS, bowlers_needed)
        team.extend(bowlers)

        remaining = size - bowlers_needed

        # Fill remaining with batters + all-rounders
        pool = BATTERS + ALL_ROUNDERS
        team.extend(random.sample(pool, remaining))

        return sorted(team)

    if mode == "batting":
        # total 3 bowlers → split randomly
        bowlers_a = random.randint(1, 2)
        bowlers_b = 3 - bowlers_a

    elif mode == "bowling":
        # total 5 bowlers
        bowlers_a = random.randint(2, 3)
        bowlers_b = 5 - bowlers_a

    else:
        # random mode
        bowlers_a = random.randint(1, 3)
        bowlers_b = random.randint(1, 3)

    team_a = build_set(6, bowlers_a)
    team_b = build_set(5, bowlers_b)

    captain = random.randint(1, 11)
    vice_captain = random.randint(1, 11)

    while vice_captain == captain:
        vice_captain = random.randint(1, 11)

    return team_a, team_b, captain, vice_captain


def generate_teams(n=5, mode="random"):
    teams = []
    for _ in range(n):
        teams.append(pick_team(mode))
    return teams


# Test run
if __name__ == "__main__":
    teams = generate_teams(5, mode="batting")
    for i, (a, b, c, vc) in enumerate(teams, 1):
        print(f"\nTeam {i}:")
        print(f"A: {a}")
        print(f"B: {b}")
        print(f"C: {c}, VC: {vc}")