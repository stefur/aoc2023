import regex as re
import math

# Get input
with open("day08.txt", "r") as file:
    # Split on double newline
    data = file.read().split("\n")


### Part 1

# First row is directions
directions = [d for d in data[0]]

paths = dict(d.split("=") for d in data[2:])

paths_split = {}
for k, v in paths.items():
    new_k = k.strip()
    new_v = v.strip().replace(")", "").replace("(", "").split(",")
    new_v = [v.strip() for v in new_v]
    paths_split.update({new_k: new_v})

steps = 0
key = "AAA"


while key != "ZZZ":
    for d in directions:
        move = paths_split[key]
        match d:
            case "R":
                key = move[1]
            case "L":
                key = move[0]
        steps += 1
        # Break early if we're not finished looping through directions
        if key == "ZZZ":
            break

print(steps)

### Part 2

# This one was tough on me, not being a math guy, so I took some hints for this one

all_keys = list(paths_split.keys())
# Find all the keys that end with A
keys = [d for d in all_keys if re.search("A$", d)]

# Create a list for steps for each of the above key
steps_for_key = []

# Loop as before, but this time over each of the keys we identified
for key in keys:
    steps = 0
    while not re.search("Z$", key):
        for d in directions:
            move = paths_split[key]
            match d:
                case "R":
                    key = move[1]
                case "L":
                    key = move[0]
            steps += 1
            # Break early if we're not finished looping through directions
            if re.search("Z$", key):
                steps_for_key.append(steps)
                break

# Use LCM (lowest common multiple) to find the answer.
result = math.lcm(*steps_for_key)
