import random
import numpy as np
import matplotlib.pyplot as plt

card_deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, "A", "J", "Q", "K"]

def draw_card(deck):
    card = random.choice(deck)
    deck.remove(card)
    return card

def draw_card_hidden(deck):
    card = random.choice(deck)
    deck.remove(card)
    return card

def shuffle(deck, full_deck):
    random.shuffle(full_deck)
    deck.clear()
    deck.extend(full_deck)

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

    while points > 21 and aces:
        points -= 10
        aces -= 1
    return points

def consider_move(player_hand, dealer_card, deck, decision_threshold):
    player_points = count_points(player_hand)
    cards_not_busting = sum(1 for card in deck if count_points(player_hand + [card]) <= 21)
    total_cards = len(deck)

    probability_safe_draw = cards_not_busting / total_cards if total_cards > 0 else 0
    return probability_safe_draw > decision_threshold

def advanced_consider_move(player_hand, dealer_card, deck, decision_threshold):
    player_points = count_points(player_hand)
    is_soft_hand = any(card == "A" for card in player_hand)

    cards_not_busting = sum(1 for card in deck if count_points(player_hand + [card]) <= 21)
    total_cards = len(deck)

    probability_safe_draw = cards_not_busting / total_cards if total_cards > 0 else 0

    thresholds = {
        "face_card": (11, 17, 0.8),
        "non_face_card": (17, 21, 0.9)
    }

    if dealer_card in ["J", "Q", "K", 10]:
        low, high, threshold_multiplier = thresholds["face_card"]
    else:
        low, high, threshold_multiplier = thresholds["non_face_card"]

    if player_points <= low:
        return True
    elif player_points >= high:
        return False

    if is_soft_hand:
        return probability_safe_draw > (decision_threshold * (threshold_multiplier * 0.9))
    else:
        return probability_safe_draw > (decision_threshold * threshold_multiplier)

def simulate_game(deck, full_deck, game_amount, decision_threshold, strategy):
    wins = 0
    draws = 0
    for _ in range(game_amount):
        if len(deck) < 15:
            shuffle(deck, full_deck)

        dealer_hand = [draw_card(deck), draw_card_hidden(deck)]
        player_hand = [draw_card(deck), draw_card(deck)]
        on_move = True

        while on_move:
            if strategy == 'advanced':
                on_move = advanced_consider_move(player_hand, dealer_hand[0], deck, decision_threshold)
            else:  # basic
                on_move = consider_move(player_hand, dealer_hand[0], deck, decision_threshold)

            if on_move:
                player_hand.append(draw_card(deck))

        player_points = count_points(player_hand)
        dealer_points = count_points(dealer_hand)
        while dealer_points < 17:
            dealer_hand.append(draw_card(deck))
            dealer_points = count_points(dealer_hand)

        # Zmodyfikowane warunki, aby uwzględnić remisy
        if player_points <= 21:
            if dealer_points > 21 or player_points > dealer_points:
                wins += 1
            elif player_points == dealer_points:
                draws += 1

    return wins, draws

def main():
    print("Wybierz ilość decków (6 to standardowa ilość):")
    deck_amount = int(input())
    full_deck = card_deck * 4 * deck_amount
    deck = full_deck.copy()

    print("Wybierz ilość gier do symulacji na każdy skok:")
    game_amount = int(input())
    print("Wybierz dolny próg decyzyjny:")
    floor_decision_threshold = float(input())
    print("Wybierz górny próg decyzyjny:")
    ceiling_decision_threshold = float(input())
    print("Wybierz skok prógów decyzyjnych:")
    decision_threshold_step = float(input())

    decision_thresholds = np.arange(floor_decision_threshold, ceiling_decision_threshold + decision_threshold_step, decision_threshold_step)
    win_rates_advanced = []
    win_rates_basic = []

    for decision_threshold in decision_thresholds:
        wins_advanced, draws_advanced = simulate_game(deck, full_deck, game_amount, decision_threshold, 'advanced')
        win_rates_advanced.append((wins_advanced / (game_amount - draws_advanced)) if (game_amount - draws_advanced) > 0 else 0)

        wins_basic, draws_basic = simulate_game(deck, full_deck, game_amount, decision_threshold, 'basic')
        win_rates_basic.append((wins_basic / (game_amount - draws_basic)) if (game_amount - draws_basic) > 0 else 0)

    plt.figure(figsize=(10, 5))
    plt.plot(decision_thresholds, win_rates_advanced, marker='o', color='blue', label='Advanced')
    plt.plot(decision_thresholds, win_rates_basic, marker='o', color='red', label='Basic')
    plt.title('Wskaźniki wygranych w zależności od progu decyzyjnego')
    plt.xlabel('Próg decyzyjny')
    plt.ylabel('Wskaźnik wygranych')
    plt.grid()

    plt.ylim(0.40, 0.46)
    max_labels = 20
    tick_indices = np.linspace(0, len(decision_thresholds) - 1, min(max_labels, len(decision_thresholds)), dtype=int)
    plt.xticks(decision_thresholds[tick_indices])

    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
