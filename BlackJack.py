import random

def restart():
    play_again = input("Would you like to play again? Yes or No: ").lower()
    if play_again == "yes": print("\n"); start();
    elif play_again == "no": exit();
    else: print("That is not a valid answer!"); restart();

def wether_to_continue(left_over, final_dealer_hand, final_player_hand, win_loss, bets):
    write_to_data(final_dealer_hand, final_player_hand, win_loss, bets)
    y_n = input("Would you like the continue? Yes or No. ").lower().strip()
    if y_n == "yes":
        play(left_over)
    elif y_n == "no":
        print("You exit with", left_over, "chips!")
        exit()
    else:
        print("That is not a valid response")
        return wether_to_continue(left_over, final_dealer_hand, final_player_hand, win_loss, bets)

def write_to_data(final_dealer_hand, final_player_hand, win_loss, bets):
    with open('blackjack_data.txt', 'a', encoding='utf-8') as file:  # Change file name here
        file.write("Outcome: {}\n".format(win_loss))
        #inverted
        file.write("Dealer hand: {}\n".format(card_formating(final_player_hand)))
        file.write("Player hand: {}\n".format(card_formating(final_dealer_hand)))
        if win_loss == "W": file.write("Amount of chips won: {}\n".format(bets))
        else: file.write("Amount of chips lost: -{}\n \n".format(bets))

def starting_chips():
    print("\n")
    betting_chips = input("How many chips would you like to play with: ")
    if betting_chips.isdigit():
        betting_chips = int(betting_chips)
        print("\n")
        return betting_chips
    else: print("that is not a valid amount of chips"); starting_chips();


def draw_card():
    deck_numbers = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
    deck_suits = ['♠', '♣', '♥', '♥']
    card_number = str(deck_numbers[random.randint(0,12)])
    card_suit = str(deck_suits[random.randint(0,3)])
    card_final = [card_number, card_suit]
    return card_final

def card_formating(hand):
    formatted_hand = ''
    for card in hand:
        formatted_hand += '[' + str(card[0]) + str(card[1]) + '], '
    return formatted_hand

def starting_hand():
    player = []
    for i in range(2):
        player.append(draw_card())
        print(card_formating(player))
        input("Continue?")
    return player

def dealers_hand():
    dealer = [draw_card()]
    return dealer

def value(hand):
    score = 0
    for digits in hand:
        if digits[0] == "K" or digits[0] == "Q" or digits[0] == "J":
            score += 10
        elif digits[0] == "A":
            ace_value = input("1 or 11: ")
            ace_value = str(ace_value).strip()
            if ace_value == "1" or ace_value == "11":
                score += int(ace_value)
            else: print("That is not a valid answer."); return value(hand);
        else:
            score += int(digits[0])
    return score

def hit(hand):
    hand.append(draw_card())

def player_choice(hand):
    while True:
        choice = input("Do you want to hit or stand: ").lower()
        choice = choice.strip()
        if choice == "hit":
            hit(hand);
            print("Players hand: ", card_formating(hand));
            if value(hand) > 21:
                return hand
        elif choice == "stand": return hand;
        else: print("That is not a valid answer");
    return hand

def dealer_choice(hand):
    total_value_d = 0
    while True:
        if value(hand) < 17: hit(hand); print("Dealer's hand:", card_formating(hand)); y = input("Continue? ")
        else:
            total_value_d = value(hand)
            return hand

def bet(left_over):
    while True:
        amount_str = input("How many chips would you like to bet: ").strip()
        if amount_str.isdigit():
            amount = int(amount_str)
            if 0 < amount <= left_over:
                print(str(amount) + "$ locked in")
                return amount
        print("Please enter a valid bet (a positive integer up to your remaining chips)")


def start():
    playing_chips = starting_chips()
    play(playing_chips)

def play(chips):
    win_loss = ''
    final_dealer_hand = []
    left_over_chips = chips
    print("Remaining Chips:", left_over_chips)
    while left_over_chips > 0:
        bets = bet(left_over_chips)
        players_hand = starting_hand()
        dealer_hand = dealers_hand()
        print("Player's hand:", card_formating(players_hand))
        print("Dealer's hand:", card_formating(dealer_hand))
        final_player_hand = player_choice(players_hand)
        final_player_hand_value = value(final_player_hand)
        if final_player_hand_value > 21:
            print("You bust!")
            left_over_chips -= bets
            win_loss = 'L'
        else:
            final_dealer_hand = dealer_choice(dealer_hand)
            final_dealer_hand_value = value(final_dealer_hand)
            if final_dealer_hand_value > 21:
                print("The dealer busts! You win!", )
                left_over_chips += bets
                win_loss = 'W'
            elif final_player_hand_value < final_dealer_hand_value or final_player_hand_value == final_dealer_hand_value:
                print("You loose,", final_dealer_hand_value, "beats", final_player_hand_value, "you loose", bets, "chips.", '\n')
                left_over_chips -= bets
                win_loss = 'L'
            else:
                print("You win,", final_player_hand_value, "beats", final_dealer_hand_value, "you gain", bets, "chips.", '\n')
                left_over_chips += bets
                win_loss = 'W'
        wether_to_continue(left_over_chips, final_player_hand, final_dealer_hand, win_loss, bets)
        if left_over_chips <= 0:
            print("You loose!")
            restart()



start()
