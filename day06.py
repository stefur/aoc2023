import regex as re
from functools import reduce

# Get input
with open("input/day06.txt", "r") as file:
    # Split on double newline
    data = file.read().split("\n")

# Split the input into a dict
games = dict(d.split(":") for d in data)

for k, v in games.items():
    # Clean values from whitespaces
    lst = v.strip()
    # A lot of whitespaces. Replace the first one with comma
    lst = re.sub(" +", ",", lst)
    # Split on comma
    lst = lst.split(",")
    # Turn it into ints
    lst = [int(x) for x in lst]
    # Put the list of values back into dict
    games.update({k: lst})

### Part 1

# A list to store the result from each race
result = []

# Go over time for each game and keep the index in x
for x, t in enumerate(games["Time"]):
    number_of_ways = []
    # Check each case where the distance is longer than the record
    for i in range(0, t):
        # Time = Time minus each hold (i) of milliseconds, i also represents speed
        travel_time = t - i
        # Calculate the distance travelled
        distance = travel_time * i
        if distance > games["Distance"][x]:
            # Append the distance to number of ways
            number_of_ways.append(distance)
    # Then append the length of that list to the result
    result.append(len(number_of_ways))

# Multiply the list items
multiply = reduce(lambda x, y: x * y, result)

# Print result
print(multiply)

### Part 2

# Correct the input according to the new info

games_2 = dict(d.split(":") for d in data)

for k, v in games_2.items():
    # Clean values from whitespaces
    val = v.strip()
    # A lot of whitespaces. Remove all of them
    val = re.sub(" ", "", val)
    # Turn it into ints
    val = int(val)
    # Put the values back into dict
    games_2.update({k: val})


# Check each case where the distance is longer than the record
for i in range(0, games_2["Time"] + 1):
    # Time = Time minus each hold (i) of milliseconds, i also represents speed
    travel_time = games_2["Time"] - i
    # Calculate the distance travelled
    distance = travel_time * i
    if distance > games_2["Distance"]:
        # Print the number of ways to beat the record
        print(travel_time - i + 1)
        break
