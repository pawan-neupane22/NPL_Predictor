import json
import os
import pandas as pd

folder = "data/processed/nepal_t20i"
files = os.listdir(folder)
matches = []
inings_rows = []
for file in files:
    if file.endswith(".json"):
        path = os.path.join(folder, file)

        with open(path, "r") as f:
            data = json.load(f)

        match_id = file.replace(".json", "")

        match = {
            "match_id": match_id,
            "season": data["info"]["season"],
            "date": data["info"]["dates"][0],
            "team_a": data["info"]["teams"][0],
            "team_b": data["info"]["teams"][1],
            "venue": data["info"]["venue"]
        }

        matches.append(match)

        innings_data = data["innings"]

        for innings in innings_data:
            for over in innings["overs"]:
                for delivery in over["deliveries"]:
                    print(delivery)