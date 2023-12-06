# Get input
with open("input/day05.txt", "r") as file:
    # Split on double newline
    data = file.read().split("\n\n")

# Split the input into a dict
locations = dict(d.split(":") for d in data)

# Go over the dict to further prepare the input
for k, v in locations.items():
    # Trim whitespace and splitlines on the string values
    lst = v.strip().splitlines()
    # Now split each item by linebreak
    lst = [i.split() for i in lst]
    # Turn all values from list of lists into ints
    lst = [[int(x) for x in row] for row in lst]
    # And update the dict with the data
    locations.update({k: lst})

### Part 1

# For simplicity just extract the seeds in a list of its own
seeds = locations.pop("seeds")[0]


# A function to go over the mappings and find the location
def find_location(seed: int, mappings: list[list]) -> int | None:
    for location in mappings:
        # For each location we range we calculate the end of source range
        source_end = location[1] + location[2] - 1

        # We check that the seed is mapped to a destination
        if location[1] <= seed <= source_end:
            # Find the destination value by subtracting the source from the seed
            # to get the difference between the two and then add it to the start of the destination range
            hit = seed - location[1] + location[0]
            return hit
        else:
            # If we find no location, the hit is seed
            hit = seed

    return hit


# A result dict
result = {"seed": [], "location": []}

# Go over each seed
for s in seeds:
    # Assign a destination variable
    destination = s
    for k in locations.keys():
        # Then use the destination to iterate over each mapping
        destination = find_location(destination, locations[k])

    # Add the result to the dict
    result["seed"].extend([s])
    result["location"].extend([destination])

# Get the lowest location
location = result["location"]
location.sort()
print(location[0])

### Part 2
# TODO
