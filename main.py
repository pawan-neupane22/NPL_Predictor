import os
import json
import pandas as pd
matches=[]
innings_rows=[]
folder = "data/raw/npl_json"
files = os.listdir(folder)
for file in files:
    if file.endswith(".json"):
        path = os.path.join(folder,file)

        with open (path,"r") as f:
            data = json.load(f)
        match_id = file.replace(".json", "")
        if "winner" in data["info"]["outcome"]:
          winner = data["info"]["outcome"]["winner"]
        else:
         winner = data["info"]["outcome"]["eliminator"]

        match = {
        "season": data["info"]["season"],
        "date":data["info"]["dates"][0],
        "team_a":data["info"]["teams"][0],
        "team_b":data["info"]["teams"][1],
        "venue":data["info"]["venue"],
        "winner":winner
        }
        matches.append(match)
        innings_data=data["innings"]
        for innings in innings_data:
            for over in innings["overs"]:
                for delivery in over["deliveries"]:
                    wickets = delivery.get('wickets')
                    if wickets:
                        wicket = 1
                        player_out = wickets[0]["player_out"]
                        wicket_kind = wickets[0]['kind']
                    else:
                        wicket = 0
                        player_out = None
                        wicket_kind = None
                    row = {
                        "match_id": match_id,
                        "batting_team":innings["team"],
                        "over":over["over"],
                        "actual_delivery": delivery["actual_delivery"],
                        "batter": delivery["batter"],
                        "bowler": delivery["bowler"],
                        "non_striker": delivery["non_striker"],
                        "batter_runs": delivery["runs"]["batter"],
                        "extra_runs": delivery["runs"]["extras"],
                        "total_runs": delivery['runs']["total"],
                        "wicket":wicket,
                        "player_out":player_out,
                        "wicket_kind":wicket_kind
                    }
                    innings_rows.append(row)
df = pd.DataFrame(matches)
df["team_a"] = df["team_a"].replace("Kathmandu Gurkhas","Kathmandu Gorkhas")
df["team_b"] = df["team_b"].replace("Kathmandu Gurkhas","Kathmandu Gorkhas")
df["winner"] = df["winner"].replace("Kathmandu Gurkhas","Kathmandu Gorkhas")
all_teams = pd.concat([df["team_a"], df["team_b"]])
df["date"] = pd.to_datetime(df["date"])
valid_winner = (df['winner']==df["team_a"]) | (df['winner']==df["team_b"])
innings_df = pd.DataFrame(innings_rows)
print("matches:", len(df))
print("deliveries:", len(innings_df))
print(innings_df.head())
print(innings_df["match_id"].nunique())






 
        




        
         
      
      
    