import regex as re

# Get input
with open("input/day04.txt", "r") as file:
    cards = file.read().splitlines()

# Split the input into a dict of games
cards_split = dict(c.split(":") for c in cards)

for card, numbers in cards_split.items():
    # Split the winning numbers vs my numbers
    numbers = numbers.split("|")
    # Trim whitespace
    numbers = [n.strip() for n in numbers]
    # Split again based on spaces
    numbers = [n.split() for n in numbers]

    # Iterate each of the two lists and convert str to int
    for lst in numbers:
        for i, n in enumerate(lst):
            lst[i] = int(n)

    # Update the dict
    cards_split.update({card: numbers})

### Part 1


# A function to check each card and calculat the points
def check_numbers(winners: [int], my_numbers: [int]) -> int:
    match = False
    points = 0

    for num in winners:
        for my_num in my_numbers:
            if num == my_num and match:
                points *= 2
            elif num == my_num:
                points += 1
                match = True
            else:
                next
    return points


# Store the result for each card
result = []

# Go over the numbers for each card and apply the function
for card_numbers in cards_split.values():
    card_points = check_numbers(card_numbers[0], card_numbers[1])
    result.append(card_points)

# Sum of the points
sum(result)

### Part 2


# A slightly modified function that returns the number of winners
def check_winners(winners: [int], my_numbers: [int]) -> int:
    wins = 0
    for num in winners:
        for my_num in my_numbers:
            if num == my_num:
                wins += 1
    return wins


# A dict for updated set of cards
updated_cards = dict()

# Update the keys to easier grab them later
for card, numbers in cards_split.items():
    card_num = re.findall(r"[0-9]", card)
    card_num = int("".join(card_num).strip())
    updated_cards.update({card_num: numbers})

# Store the number of copies for each card
card_copies = dict()

# Store the number of all cards including copies
result = []

# Not very efficient but gets the job done so... :)

# Iterate of dict of cards and numbers
for card, card_numbers in updated_cards.items():
    # Check if there are any present copies of the card
    try:
        number_of_copies = card_copies[card]
    except KeyError:  # Card might not exist as a copy
        number_of_copies = 1  # Set it to 1 so we iterate once
        # And also this number will be appended as the original still counts if there is no win
    for copy in range(0, number_of_copies):
        # Get the number of wins
        card_wins = check_winners(card_numbers[0], card_numbers[1])
        if card_wins > 0:
            # If there's at least 1 win we calculate the range of the next cards
            next_card = card + 1  # Next card in line to copy
            last_card = next_card + card_wins  # The last card to copy
            # Iterate the range of those cards (keys as ints come into play here)
            for i in range(next_card, last_card):
                # Check for any existing number of copies of those cards
                try:
                    existing_copies = card_copies[i]
                except KeyError:
                    existing_copies = 1
                card_copies.update({i: existing_copies + 1})  # Add a copy

    # In the end we append the number of copies for the given card
    result.append(number_of_copies)

# Get the finished sum
sum(result)
