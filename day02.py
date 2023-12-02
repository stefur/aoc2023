import regex as re
from functools import reduce

# Get input
with open("input/day02.txt", "r") as file:
    games = file.read().splitlines()

# Split the input into a dict of games
games_split = dict(g.split(":") for g in games)

# Split the different games into sets and trim whitespace from each set
for game, sets in games_split.items():
    sets = sets.split(";")
    sets = [s.strip() for s in sets]
    games_split.update({game: sets})

### Part 1


def extract_possible_games(color_sets: list, colors: list) -> list | None:
    # Create a list to store all the sets
    all_sets = []
    for s in color_sets:
        # Set up a new dict to split key and value
        color_set = {}
        # For each color that we want to use as key
        for color in colors:
            # Try to extract the element containing the value
            try:
                value = int(re.findall(f"([0-9]+) {color}", s)[0])

                # Return None if any color/value combination are exceeds limit
                if any(
                    [
                        color == "red" and value > 12,
                        color == "green" and value > 13,
                        color == "blue" and value > 14,
                    ]
                ):
                    return None

                color_set.update({f"{color}": value})

            except IndexError:
                # This can cause index error in case the color doesn't exist, then we just pass
                pass
        # We add the completed color set to list of all sets
        all_sets.append(color_set)
    return all_sets


# Create a list of our colors to use as keys
colors = ["red", "green", "blue"]

# And a dict to store the result
result = {}

# Iterate items of the games
for game, sets in games_split.items():
    sets = extract_possible_games(sets, colors)

    # If we got something in return from our function...
    if sets is not None:
        # ...update our dict of results with sets all set up
        result.update({game: sets})

# The sum of possible ID stored in a list
sum_of_id = []

# Find the number in the game ID and store it
for game in result.keys():
    id_value = int(re.findall("[0-9]+", game)[0])
    sum_of_id.append(id_value)

# Get the sum of the ID's
sum(sum_of_id)

### Part 2


# A modified function
def fewest_possible(color_sets: list, colors: list) -> int:
    # Create a dict to store the resulting color values for each game
    fewest = {}

    # For each color that we want to use as key like in part 1
    for color in colors:
        # Define a top_value that we are going to find
        top_value = 0

        # Go over the sets of color
        for s in color_sets:
            # Try to extract the element containing the value
            try:
                value = int(re.findall(f"([0-9]+) {color}", s)[0])

                # If our value is greater than the top_value we replace it
                if value > top_value:
                    top_value = value

            except IndexError:
                # This can cause index error in case the color doesn't exist, then we just pass
                pass
        # We add the completed color set to list of all sets
        fewest.update({color: top_value})

    # Multiply all the values together
    power = reduce(lambda x, y: x * y, fewest.values())

    return power


# Create a list of our colors
colors = ["red", "green", "blue"]

# And a dict to store the result
result = {}

# Iterate items of the games
for game, sets in games_split.items():
    # Get the fewest possible colors
    fewest_possible_colors = fewest_possible(sets, colors)

    # Update our result dict for each game
    result.update({game: fewest_possible_colors})

# Get the result of the values
sum(result.values())
