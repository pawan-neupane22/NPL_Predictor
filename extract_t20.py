import json
import os
folder="data/raw/nepal_male_json"
files=os.listdir(folder)
for file in files:
    path = os.path.join(folder,file)
    with open(path) as f:
        data =json.load (f)
        date = data["info"]["dates"][0]
        print(date,data["info"]["match_type"])

    