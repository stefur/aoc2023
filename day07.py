from enum import Enum
from dataclasses import dataclass, field

# Get input
with open("input/day07.txt", "r") as file:
    # Split on double newline
    data = file.read().split("\n")

### Part 1


class Rank(Enum):
    FIVE_OF_A_KIND = 1
    FOUR_OF_A_KIND = 2
    FULL_HOUSE = 3
    THREE_OF_A_KIND = 4
    TWO_PAIR = 5
    ONE_PAIR = 6
    HIGH_CARD = 7


# Dataclass to hold values to count when going over the cards.
@dataclass
class Cards:
    values: dict = field(
        default_factory=lambda: {
            "A": 0,
            "K": 0,
            "Q": 0,
            "J": 0,
            "T": 0,
            "9": 0,
            "8": 0,
            "7": 0,
            "6": 0,
            "5": 0,
            "4": 0,
            "3": 0,
            "2": 0,
        }
    )


def check_cards(cards: [str]) -> dict | None:
    # Instantiate Cards
    c = Cards()
    # Pick up the default dict to use
    card_types = c.values

    # Count types of card for the given hand
    for c in cards:
        if c in card_types.keys():
            card_types[c] += 1

    # Remove any cards that are not present in hand
    on_hand = {k: v for k, v in card_types.items() if v >= 1}

    # Result of the function can be none if there's no win
    result = None

    # If we have any combinations on hand
    if on_hand:
        on_hand_values = list(on_hand.values())

        # Check for full house, high_card and so on...

        if any(v == 2 for v in on_hand_values) and any(v == 3 for v in on_hand_values):
            result = Rank.FULL_HOUSE

        elif on_hand_values.count(1) == 5:
            result = Rank.HIGH_CARD

        elif on_hand_values.count(2) == 1:
            result = Rank.ONE_PAIR

        elif on_hand_values.count(2) == 2:
            result = Rank.TWO_PAIR

        elif on_hand_values.count(5) == 1:
            result = Rank.FIVE_OF_A_KIND

        elif on_hand_values.count(4) == 1:
            result = Rank.FOUR_OF_A_KIND

        elif on_hand_values.count(3) == 1:
            result = Rank.THREE_OF_A_KIND

    return result


hands = dict(d.split(" ") for d in data)

# Go over the hands to determine possible types of wins
for k, v in hands.items():
    c = check_cards(k)
    hands.update({k: (v, c)})

# Create the sort order according to the previously defined card_types
sort_order = {}
i = 0
# Use the keys in the dataclass dict to create the order enumerated
for k in Cards().values.keys():
    sort_order.update({k: i})
    i += 1


# A function to help with the sorting
def sort_cards(cards):
    return [sort_order[c] for c in cards]


# Iterate over each type or rank of win, keep the orderd bids in a list
bids = []
for n in Rank:
    # Here I was stuck for a good amount of time.
    # Didn't properly and assumed the no win hands should
    # be discarded. This was wrong!
    # if n == Rank.NO_WIN:
    #   continue

    # Filter out matching hands for the rank
    matching_hands = [k for k, v in hands.items() if v[1] == n]

    # Sort the cards given the value of each card
    sorted_cards = sorted(matching_hands, key=sort_cards)
    # Take the sorted cards and append to result
    for card in sorted_cards:
        bids.append(int(hands[card][0]))


# Reverse the entire list to get worst to best hand in correct order for the final step
bids.reverse()

# Now multiply the bids in the list with their
for i in range(0, len(bids)):
    bids[i] = bids[i] * (i + 1)

# Get the sum
sum(bids)


### Part 2


# Dataclass to hold values to count when going over the cards.
@dataclass
class CardsRevised:
    values: dict = field(
        default_factory=lambda: {
            "A": 0,
            "K": 0,
            "Q": 0,
            "T": 0,
            "9": 0,
            "8": 0,
            "7": 0,
            "6": 0,
            "5": 0,
            "4": 0,
            "3": 0,
            "2": 0,
            "J": 0,
        }
    )


def check_cards_jokers(cards: [str]) -> dict | None:
    # Instantiate Cards
    c = CardsRevised()
    # Pick up the default dict to use
    card_types = c.values

    # Count types of card for the given hand
    for c in cards:
        if c in card_types.keys():
            card_types[c] += 1

    # Remove any cards that are not present in hand
    on_hand = {k: v for k, v in card_types.items() if v >= 1}

    # Taking the easy way out for an edge case:
    # If it's all jokers just return five of a kind
    if all(k == "J" for k in on_hand.keys()):
        return Rank.FIVE_OF_A_KIND

    # Adapted to handle jokers
    if any(k == "J" for k in on_hand.keys()):
        # Get the (key) card with most cards
        top_card = sorted(on_hand, key=on_hand.get)[-1]
        i = 1
        # Get the next top card in line while top card is J
        while top_card == "J" and i < len(on_hand) + 1:
            top_card = sorted(on_hand, key=on_hand.get)[-i]
            i += 1

        # Add the value of jokers to that card
        on_hand[top_card] = on_hand[top_card] + on_hand["J"]

    # Result of the function can be none if there's no win
    result = None

    # If we have any combinations on hand
    if on_hand:
        on_hand_values = list(on_hand.values())

        # Now check for full house, high_card and so on...
        # This is adapted to correctly match on rank
        if any(k != "J" and v == 2 for k, v in on_hand.items()) and any(
            k != "J" and v == 3 for k, v in on_hand.items()
        ):
            result = Rank.FULL_HOUSE

        elif on_hand_values.count(5) == 1:
            result = Rank.FIVE_OF_A_KIND

        elif on_hand_values.count(4) == 1:
            result = Rank.FOUR_OF_A_KIND

        elif on_hand_values.count(3) == 1:
            result = Rank.THREE_OF_A_KIND

        elif on_hand_values.count(2) == 2:
            result = Rank.TWO_PAIR

        elif on_hand_values.count(2) == 1:
            result = Rank.ONE_PAIR

        elif on_hand_values.count(1) == 5:
            result = Rank.HIGH_CARD

    return result


hands_revised = dict(d.split(" ") for d in data)

# Go over the hands to determine possible types of wins
for k, v in hands_revised.items():
    c = check_cards_jokers(k)
    hands_revised.update({k: (v, c)})

# Create the sort order according to the previously defined card_types
sort_order = {}
i = 0
# Use the keys in the dataclass dict to create the order enumerated
for k in CardsRevised().values.keys():
    sort_order.update({k: i})
    i += 1


# A function to help with the sorting
def sort_cards(cards):
    return [sort_order[c] for c in cards]


# Iterate over each type or rank of win, keep the orderd bids in a list
bids = []
for n in Rank:
    # Filter out matching hands for the rank
    matching_hands = [k for k, v in hands_revised.items() if v[1] == n]

    # Sort the cards given the value of each card
    sorted_cards = sorted(matching_hands, key=sort_cards)

    # Take the sorted cards and append to result
    for card in sorted_cards:
        bids.append(int(hands_revised[card][0]))


# Reverse the entire list to get worst to best hand in correct order for the final step
bids.reverse()

# Now multiply the bids in the list with their
for i in range(0, len(bids)):
    bids[i] = bids[i] * (i + 1)

# Get the sum
sum(bids)
