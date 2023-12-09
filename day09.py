# Get input
with open("input/day09.txt", "r") as file:
    data = file.read().splitlines()
    # Split each row into a list of items
    data = [list(map(int, d.split(" "))) for d in data]

### Part 1

# A list to keep results of each row
result = []

# Go over the rows
for row in data:
    # The last sequence is the row
    last_sequence = row
    # Keep the row results in a list
    row_result = []

    # All numbers in the last sequence must be equal to 0
    while not all(x == 0 for x in last_sequence):
        next_sequence = []
        # Calculate the difference for next sequence
        for i, x in enumerate(last_sequence):
            # Don't go out of bounds
            if i + 1 < len(last_sequence):
                diff = last_sequence[i + 1] - x
                next_sequence.append(diff)

        # Set the last sequence to this one
        last_sequence = next_sequence
        # And append it to the result
        row_result.append(last_sequence)

    # Time to calculate history, that means iterating in reverse
    history_sequence = []
    row_result.reverse()

    # Go over each sequence of the row result
    for n, r in enumerate(row_result):
        # Handle the first row
        if n - 1 <= 0:
            history = r[-1]
        else:
            # Otherwise calculate the next number in the sequence by adding the
            # last number to the the last previous number
            history = r[-1] + history_sequence[-1]

        # Append the history
        history_sequence.append(history)

    # When we're done we can get the final history in the sequence by taking
    # the last number of the history sequence and adding it to the last number in the row we're on
    final_history = history_sequence[-1] + row[-1]

    # Add it to our result list
    result.append(final_history)

# Sum it all up
sum(result)


### Part 2

# This is all basically the same as part 1, with very small modifications
# handling the history sequence.

# A new list for the next part
result = []

# Go over the rows
for row in data:
    # The last sequence is the row
    last_sequence = row
    # Keep the row results in a list
    row_result = []

    # All numbers in the last sequence must be equal to 0
    while not all(x == 0 for x in last_sequence):
        next_sequence = []
        # Calculate the difference for next sequence
        for i, x in enumerate(last_sequence):
            # Don't go out of bounds
            if i + 1 < len(last_sequence):
                diff = last_sequence[i + 1] - x
                next_sequence.append(diff)

        # Set the last sequence to this one
        last_sequence = next_sequence
        # And append it to the result
        row_result.append(last_sequence)

    # Time to calculate history, that means iterating in reverse
    history_sequence = []
    row_result.reverse()

    # Go over each sequence of the row result
    for n, r in enumerate(row_result):
        # Handle the first row
        if n - 1 <= 0:
            history = r[0]
        else:
            # Otherwise calculate the next number in the sequence by removing the
            # first number from the the first previous number
            history = r[0] - history_sequence[0]

        # Now insert the history to the first position of the list instead
        history_sequence.insert(0, history)

    # When we're done we can get the final history in the sequence by taking
    # the first number in the row we're on minus the first number in the history sequence
    final_history = row[0] - history_sequence[0]

    # Add it to our result list
    result.append(final_history)

sum(result)
