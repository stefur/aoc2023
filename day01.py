# Use a regex lib
import regex as re

# Get input
with open("input/day01.txt", "r") as file:
    calibration_values = file.read().splitlines()


### Part 1

# Store the extracted calibration values
result = []

# For each value, regex the digits and take
# the first and last element to store in the list
for value in calibration_values:
    num = re.findall(r"[0-9]", value)
    result.append(int(num[0] + num[-1]))

# Get the sum of the result
sum(result)

### Part 2

# Another go for results
result = []

translation = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

for value in calibration_values:
    # Find overlapping values
    num = re.findall(
        r"[0-9]|one|two|three|four|five|six|seven|eight|nine", value, overlapped=True
    )
    first_and_last = [num[0], num[-1]]
    for i, s in enumerate(first_and_last):
        # Translate stuff
        if s in translation:
            first_and_last[i] = translation[s]
    # Append it by joining the numbers
    result.append(int("".join(x for x in first_and_last)))

sum(result)
