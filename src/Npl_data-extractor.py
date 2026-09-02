import os
import json 
import pandas as pd

matches = []
innings_rows = []

folder = "data/raw/npl_json"
files = os.listdir(folder)

for file in files:
    if file.endswith(".json"):
        path = os.path.join(folder, file)

        with open(path, "r") as f:
            data = json.load(f)

        match_id = file.replace(".json", "")

        if "winner" in data["info"]["outcome"]:
            winner = data["info"]["outcome"]["winner"]
        else:
            winner = data["info"]["outcome"]["eliminator"]

        match = {
            "match_id": match_id,
            "season": data["info"]["season"],
            "date": data["info"]["dates"][0],
            "team_a": data["info"]["teams"][0],
            "team_b": data["info"]["teams"][1],
            "venue": data["info"]["venue"],
            "winner": winner
        }

        matches.append(match)

        innings_data = data["innings"]

        for innings in innings_data:
            for over in innings["overs"]:
                for delivery in over["deliveries"]:
                    if delivery["runs"]["batter"] == 4:
                        four = 1
                    else:
                        four = 0

                    if delivery["runs"]["batter"] == 6:
                        six = 1
                    else:
                        six = 0
                    extras = delivery.get("extras",{})
                    if "byes" in extras or "legbyes" in extras:
                      bowler_runs = 0
                    else:
                     bowler_runs = delivery["runs"]["total"]
                    
                    extras = delivery.get("extras",{})
                    if "wides" in extras or "noballs" in extras:
                        legal_ball = 0
                    else:
                        legal_ball = 1
                    if legal_ball ==1 and delivery['runs']["total"]== 0:
                        dot_ball = 1
                    else:
                        dot_ball = 0

                    wickets = delivery.get("wickets")

                    if wickets:
                        wicket = 1
                        player_out = wickets[0]["player_out"]
                        wicket_kind = wickets[0]["kind"]
                    else:
                        wicket = 0
                        player_out = None
                        wicket_kind = None
                    if wicket_kind in ["caught", "bowled", "lbw", "stumped","caught and bowled", "hit wicket"]:
                       bowler_wicket = 1
                    else:
                      bowler_wicket = 0
                    if player_out == delivery["batter"]:
                        dismiss=1
                    else:
                        dismiss=0

                    row = {
                        "match_id": match_id,
                        "batting_team": innings["team"],
                        "over": over["over"],
                        "actual_delivery": delivery["actual_delivery"],
                        "batter": delivery["batter"],
                        "bowler": delivery["bowler"],
                        "non_striker": delivery["non_striker"],
                        "batter_runs": delivery["runs"]["batter"],
                        "extra_runs": delivery["runs"]["extras"],
                        "total_runs": delivery["runs"]["total"],
                        "wicket": wicket,
                        "player_out": player_out,
                        "wicket_kind": wicket_kind,
                        "legal_ball": legal_ball,
                        "dismiss": dismiss,
                        "extra_type":list(extras.keys())[0] if extras else None,
                        "bowler_runs": bowler_runs,
                        "bowler_wicket": bowler_wicket,
                        "dot_ball":dot_ball,
                        "four": four,
                        "six": six

                    }

                    innings_rows.append(row)


df = pd.DataFrame(matches)
innings_df = pd.DataFrame(innings_rows)

df["team_a"] = df["team_a"].replace(
    "Kathmandu Gurkhas",
    "Kathmandu Gorkhas"
)

df["team_b"] = df["team_b"].replace(
    "Kathmandu Gurkhas",
    "Kathmandu Gorkhas"
)

df["winner"] = df["winner"].replace(
    "Kathmandu Gurkhas",
    "Kathmandu Gorkhas"
)

innings_df["batting_team"] = innings_df["batting_team"].replace(
    "Kathmandu Gurkhas",
    "Kathmandu Gorkhas"
)

df["date"] = pd.to_datetime(df["date"])
player_runs = innings_df.groupby("batter")["batter_runs"].sum()
balls_faced = innings_df.groupby("batter")["legal_ball"].sum()
strike_rate = (player_runs / balls_faced) * 100
dismissals = innings_df.groupby("batter")['dismiss'].sum()
batting_average = player_runs / dismissals
balls_bowled = innings_df.groupby("bowler")["legal_ball"].sum()
conceded_runs = innings_df.groupby("bowler")["bowler_runs"].sum()
economy =(conceded_runs/balls_bowled)*6
bowler_wickets =innings_df.groupby('bowler')["bowler_wicket"].sum()
dot_balls=innings_df.groupby("bowler")["dot_ball"].sum()
bowling_strike_rate =balls_bowled/bowler_wickets
fours = innings_df.groupby("batter")["four"].sum()
sixes = innings_df.groupby("batter")["six"].sum()
boundary_runs = (fours * 4) + (sixes * 6)
player_profile = pd.concat(
    [
        player_runs,
        balls_faced,
        strike_rate,
        dismissals,
        fours,
        sixes,
        balls_bowled,
        conceded_runs,
        economy,
        bowler_wickets,
        dot_balls,
        bowling_strike_rate
    ],
    axis=1
)

player_profile.columns = [
    "runs",
    "balls_faced",
    "strike_rate",
    "dismissals",
    "fours",
    "sixes",
    "balls_bowled",
    "bowler_runs",
    "economy",
    "bowler_wickets",
    "dot_balls",
    "bowling_strike_rate"
]
print(player_profile.head(10))