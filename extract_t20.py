import json
import os

folder = "data/raw/nepal_male_json"
output = "data/processed/nepal_t20i"

files = os.listdir(folder)

count = 0

for file in files:
    if file.endswith(".json"):
        path = os.path.join(folder, file)

        with open(path) as f:
            data = json.load(f)

        date = data["info"]["dates"][0]
        match_type = data["info"]["match_type"]

        if date >= "2018-01-01" and match_type in ["T20", "IT20"]:
            output_path = os.path.join(output, file)

            with open(output_path, "w") as f:
                json.dump(data, f, indent=2)

            count = count + 1

print("Total T20/IT20 matches:", count)
