import regex as re
from functools import reduce

# Get input
with open("input/day03.txt", "r") as file:
    schematic = file.read().splitlines()

### Part 1

# Hacky solution that should inspire no one.
lookup = r"^(?!.*?[0-9]|.*\.).*"
result = []
val = []

start_pos = 0
end_pos = 0

for x, row in enumerate(schematic):
    # Get the previous andnext rows if not out of bounds
    prev_row = schematic[x - 1] if x > 0 else None
    next_row = schematic[x + 1] if x < len(schematic) - 1 else None

    # Get this row
    this_row = list(row)

    this_row_result = []

    # Move along the schematic for parts
    for y, part in enumerate(this_row):
        # Either not a digit or a digit with a y coordinate within bounds
        if not part.isdigit() or (part.isdigit() and y == len(this_row) - 1):
            if part.isdigit():
                # Append the digit to value
                val.append(part)
            # If there is a value
            if val:
                # Make it a string
                s = "".join(val)
                # And move the end position up 1 step
                end_pos += 1

                checks = []

                # Check adjacent characters with this horrible try iteration
                try:
                    next_char = this_row[end_pos - 1]
                    if re.search(lookup, next_char):
                        checks.append(True)
                except IndexError:
                    pass

                try:
                    prev_char = this_row[start_pos]
                    if re.search(lookup, prev_char):
                        checks.append(True)

                except IndexError:
                    pass

                try:
                    prev_row_values = list(prev_row[start_pos:end_pos])
                    if any(re.search(lookup, x) for x in prev_row_values):
                        checks.append(True)
                except TypeError:
                    pass

                try:
                    next_row_values = list(next_row[start_pos:end_pos])
                    if any(re.search(lookup, x) for x in next_row_values):
                        checks.append(True)
                except TypeError:
                    pass

                # If any of the above passed as true
                if any(checks) is True:
                    this_row_result.append(s)
                # Append the result and empty the list to start over
                val = []

            # Also handle coordinates for bounds
            if y == len(this_row) - 1:
                start_pos = 0
                end_pos = 1
            else:
                start_pos = y
                end_pos = y + 1

        # Look for numbers
        num = re.findall(r"[0-9]", part)

        if num:
            val.append(num[0])
            end_pos += 1

    result.append(this_row_result)

total_sum = []
for row in result:
    row_sum = sum([int(r) for r in row])
    total_sum.append(row_sum)

sum(total_sum)


### Part 2


def scan_gears(schematics: list, x: int, y: int) -> list | None:
    directions = {
        "right": (x, y + 1),
        "left": (x, y - 1),
        "top": (x - 1, y),
        "bottom": (x + 1, y),
        "top_left": (x - 1, y - 1),
        "top_right": (x - 1, y + 1),
        "bottom_left": (x + 1, y - 1),
        "bottom_right": (x + 1, y + 1),
    }
    # A list to store already scanned coordinates
    already_scanned = []
    result = []
    for d, c in directions.items():
        gear = []

        # This is the position we're checking
        try:
            num = schematics[c[0]][c[1]]
            # Check that the number we got is indeed a digit and not already scanned
            if num.isdigit() and (c[0], c[1]) not in already_scanned:
                gear.append(num)
            else:
                continue
        # But it could be out of bounds. So a simple try will do to check.
        except IndexError:
            continue

        # Bounds of a row, should be 0 - 139 given length of 140
        bounds = (0, len(schematics[c[0]]) - 1)

        # Counters for moving left and right
        r = 1
        l = 1

        # Check right for any digits to append assuming that the next step is within bounds
        while c[1] + r <= bounds[1]:
            right = schematics[c[0]][c[1] + r]
            if right.isdigit() and (c[0], c[1] + r) not in already_scanned:
                gear.append(right)
                already_scanned.append((c[0], c[1] + r))
                r += 1
            else:
                break

        # Do the same for left
        while c[1] - l >= bounds[0]:
            left = schematics[c[0]][c[1] - l]
            if left.isdigit() and (c[0], c[1] - l) not in already_scanned:
                gear.insert(0, left)
                already_scanned.append((c[0], c[1] - l))
                l += 1

            else:
                break

        # Join the gear numbers into a string
        gear = "".join(gear)
        result.append(gear)

    # If we found more than one gear we return the result
    if len(result) > 1:
        return result


# A list to keep all the gear pairs
all_gears = []

# Go over the coordinates in the schematic
for x, row in enumerate(schematic):
    this_row = list(row)
    for y, char in enumerate(this_row):
        # If we hit a * we get the coordinates
        if re.search(r"\*", char):
            # Scan for gears around the coordinate
            gear_coords = scan_gears(
                schematic,
                x,
                y,
            )
            if gear_coords is not None:
                all_gears.append(gear_coords)


total_sum = []
for gears in all_gears:
    # Multiply  the ratios
    ratio = reduce(lambda x, y: int(x) * int(y), gears)
    total_sum.append(ratio)

# Sum fo the ratios
sum(total_sum)
