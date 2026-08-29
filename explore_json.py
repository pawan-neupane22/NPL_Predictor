import json

# Open the JSON file
with open("1511008.json", "r") as file:
    match = json.load(file)

# Basic information
print("Teams:", match["info"]["teams"])
print("Date:", match["info"]["dates"])
print("Venue:", match["info"]["venue"])
print("Toss:", match["info"]["toss"])
print("Winner:", match["info"]["outcome"]["winner"])

# Players
print("\nPlayers:")
for team, players in match["info"]["players"].items():
    print(team)
    for player in players:
        print("  ", player)