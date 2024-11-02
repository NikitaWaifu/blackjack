import random
import numpy as np
import matplotlib.pyplot as plt

card_deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, "A", "J", "Q", "K"]


def draw_card(deck, known_deck):
    card = random.choice(deck)
    deck.remove(card)
    known_deck.remove(card)
    return card


def draw_card_hidden(deck):
    card = random.choice(deck)
    deck.remove(card)
    return card


def shuffle(deck, full_deck, known_deck):
    deck.clear()
    deck.extend(full_deck)
    known_deck.clear()
    known_deck.extend(full_deck)


def count_points(hand):
    points = 0
    aces = 0
    for card in hand:
        if card in ["J", "Q", "K"]:
            points += 10
        elif card == "A":
            aces += 1
            points += 11
        else:
            points += card

    # Adjust for Aces if points exceed 21
    while points > 21 and aces:
        points -= 10
        aces -= 1
    return points


def consider_move(player_hand, dealer_card, deck, decision_threshold):
    player_points = count_points(player_hand)
    cards_not_busting = 0
    total_cards = len(deck)

    # Simulate card drawing
    for card in deck:
        player_hand.append(card)
        if count_points(player_hand) <= 21:
            cards_not_busting += 1
        player_hand.pop()

    # Calculate the probability of drawing a non-busting card
    probability_safe_draw = cards_not_busting / total_cards

    # Decide to hit or stay based on probability
    return probability_safe_draw > decision_threshold


# Input
print("Wybierz ilość decków (6 to standardowa ilość):")
deck_amount = int(input())
full_deck = card_deck * 4 * deck_amount
deck = full_deck.copy()
known_deck = full_deck.copy()

print("Wybierz ilość gier do symulacji na każdy skok:")
game_amount = int(input())
print("Wybierz dolny próg decyzyjny:")
floor_decision_threshold = float(input())
print("Wybierz górny próg decyzyjny:")
ceiling_decision_threshold = float(input())
print("Wybierz skok prógów decyzyjnych:")
decision_threshold_step = float(input())

decision_thresholds = np.arange(floor_decision_threshold, ceiling_decision_threshold + decision_threshold_step,
                                decision_threshold_step)
win_rates = []

for decision_threshold in decision_thresholds:
    wins = 0
    losses = 0
    draws = 0
    for i in range(game_amount):
        on_move = True
        if len(deck) < 15:
            shuffle(deck, full_deck, known_deck)

        # Initial hands
        dealer_hand = [draw_card(deck, known_deck), draw_card_hidden(deck)]
        player_hand = [draw_card(deck, known_deck), draw_card(deck, known_deck)]

        # Player's turn
        while on_move:
            on_move = consider_move(player_hand, dealer_hand[0], known_deck, decision_threshold)
            if on_move:
                player_hand.append(draw_card(deck, known_deck))

        player_points = count_points(player_hand)

        # Dealer's turn
        dealer_points = count_points(dealer_hand)
        while dealer_points < 17:
            dealer_hand.append(draw_card(deck, known_deck))
            dealer_points = count_points(dealer_hand)

        # Game result
        if player_points > 21:
            losses += 1
        elif dealer_points > 21 or player_points > dealer_points:
            wins += 1
        elif player_points < dealer_points:
            losses += 1
        else:
            draws += 1

    # Store win rate
    win_rates.append(wins / game_amount)

# Plot results
plt.figure(figsize=(10, 5))
plt.plot(decision_thresholds, win_rates, marker='o')
plt.title('Wskaźniki wygranych w zależności od progu decyzyjnego')
plt.xlabel('Próg decyzyjny')
plt.ylabel('Wskaźnik wygranych')
plt.grid()

# Ustalenie maksymalnie 20 etykiet
max_labels = 20
tick_indices = np.linspace(0, len(decision_thresholds) - 1, min(max_labels, len(decision_thresholds)), dtype=int)
plt.xticks(decision_thresholds[tick_indices])

plt.show()
