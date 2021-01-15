"""
    Assignment #5: Blackjack

    Please read 'help_message' below for the rules of the game.

    Games starts with user's input of Y (yes), N (no), or H (help)

"""

from random import shuffle # tro generate random integer
import time  # to use sleep() - time delay
import os  # to use screen clear function



# to use unicode for suits of card
card_suit = {1:"\u2660", 2:"\u2665", 3:"\u2666", 4:"\u2663"}

# set values for card name:
card_deck = {1:"A", 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8,
9:9, 10:10, 11:"J", 12:"Q", 13:"K"}

# set values of each card
card_value = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8,
9:9, 10:10, 11:10, 12:10, 13:10}

# variable used in statistics, how many times player/dealer won.
count_player_win = [0] # total number of wins for player
count_dealer_win = [0] # total number of wins for dealer
count_tie_score = [0]

card_pile, player_pile, dealer_pile, player_split_pile =[], [], [], []  # to hold one deck of cards


# Loop to ask player to play continually and calling a function accordingly
def main():
    ''' Starting the program '''
    help_message = '''
Here are rules:
The objective of the game is to draw cards and obtain the highest total not exceeding 21.
The game uses two decks of cards.
The value of J, Q, and K is 10. Ace can have value either 1 or 11.
The game begins by dealing two visible cards to the player (face up), and two to the dealer.
However, one of dealer's card is visible to the player while the other is hidden.
When player's has the same value in the first two card, player can split.
The player decides whether to "hit" (draw another card), or "stand" which ends their turn.
The player may hit any number of times.
Should the total of the cards exceed 21, the player "busts" and loses the game to the dealer.
If the player reaches 21, the player stands.
The dealer's turn begins by revealing the hidden card.
The dealer must continue to hit if the total is 16 or less.
The deal will stand if the value is 17 or more.
The dealer busts if their total is over 21 and the player wins.
The dealer wins all ties (i.e. if both the dealer and the player reach 21, the dealer wins).
The program indicates who the winner is and asks to play again
'''
    welcome_sign()

    shuffle_cards() # to generate the card decks

    # Ask player whether he wants to play or continuoysly play
    while True:

        # asking player for the continuous player
        print ()
        continue_decision = input ('Do you want to play, y(Yes)/ n(No)/ h(Help)? ')
        continue_decision = continue_decision.replace (" ", "") #remove space from input

        if len(card_pile) < 10: # adding new cards when remaining cards are low
            print ("\nOops! The remaining cards are less than 10.")
            print ("Discarding remaing cards and Shuffling two new sets of cards.")
            card_pile.clear()
            shuffle_cards()
            time.sleep(3)

        if continue_decision.lower() in ("y", "yes"):
            draw_line_message (banner="")
            play_black_jack()

        elif continue_decision.lower() in ("n", "no"):
            os.system ('cls')
            draw_line_message (banner="Thank you for playing!")
            break

        elif continue_decision.lower() in ("h", "help"):
            print (help_message)

        # message for user to select only y, n, or h
        else:
            print ('\n\nPleas enter y(yes) or n(no) or h(help).')
            time.sleep(1)

def shuffle_cards ():
    """ generate card pile for play
        tuple = (card suit, number, value)
        it will generate two decks of cards
    """
    for deck in range (2):
        for suit in range (1,5):
            for number in range (1, 14):
                if number > 10:
                    card_pile.append((suit, number, 10 ))
                else:
                    card_pile.append((suit, number, number))
        shuffle (card_pile)


def dispense_card (whose_turn):
    """ Distributing cards to either player or dealer
    and adjusting the value of Ace card """

    distribution = card_pile.pop(0) # remove the first card in the pile

    if whose_turn == "player":
        player_pile.append (distribution)
        temp_sum = calculate_total (player_pile)
        if (player_pile[0][0] > 0) and (player_pile[-1][2] == 1):#ace adjustment in position 0
            if temp_sum < 12:
                player_pile.insert(0, (0,0,10))  #put ace tracker in position 0


    elif whose_turn == "split":
        player_split_pile.append (distribution)

        #to adjust value of Ace
        temp_sum = calculate_total (player_split_pile)
        if (player_split_pile[0][0] > 0) and player_split_pile[-1][2] == 1:
            if temp_sum < 12:
                player_split_pile.insert(0, (0,0,10)) #put ace tracker in position 0


    elif whose_turn == "dealer":
        dealer_pile.append (distribution)
        temp_sum = calculate_total (dealer_pile)
        if (dealer_pile[0][0] > 0) and (dealer_pile[-1][2] == 1):#ace adjustment in position 0
            if temp_sum < 12:
                dealer_pile.insert(0, (0,0,10)) #put ace tracker in position 0



    return distribution


def first_cards ():
    ''' Starting first two cards'''

    # generating the first two cards for player and dealer
    for i in range (2):
        dispense_card ("player")
        dispense_card ("dealer")

    #  to check Balckjack
    if player_pile[0][0] == 0:
        if (player_pile[-2][1] > 10) or (player_pile[-1][1] > 10):
            print ('You have Blackjack!!! \n')

    player_total = calculate_total (player_pile)
    print (f'You draw a {card_suit[player_pile[-2][0]]}{card_deck[player_pile[-2][1]]} \
and a {card_suit[player_pile[-1][0]]}{card_deck[player_pile[-1][1]]}. \
Your total is {player_total}.')


    print (f'Dealer draws a {card_suit[dealer_pile[-2][0]]}{card_deck[dealer_pile[-2][1]]} \
and a hidden card. \n')


def calculate_total (whose_turn):
    '''calculate the current total'''
    total = 0

    for card in whose_turn:
        total += card [2]

    return total

# function to play black jack
def play_black_jack ():
    '''
    logics and loops of black jack
    '''

    player_pile.clear()
    dealer_pile.clear()
    player_split_pile.clear()

    first_cards ()


    # chck for split decision
    if player_pile[-2][1] == player_pile[-1][1]:
        split_decision = "y"
    else:
        split_decision = "n"

    #Split play
    dealer_play = "y" #set the defaul value for dealer turn
    if split_decision == "y":
        while True:
            split_decision = input ('Do you want to split (y/n)?')

            if split_decision.lower() not in ("y", "n"):
                print ('Please enter Y or N for split play.')

            elif split_decision.lower() == "n":
                player_total = player_turn (split_decision)
                break

            else: #if split_decision.lower() == "y":

                print ('\nPlaying Set #1')
                split_card = player_pile.pop(-1)
                player_split_pile.append(split_card)
                player_total_split = player_turn_split ()

                print ('\nYour total from Set_1 is', player_total_split)

                print ('\nPlaying Set #2')

                player_total = player_turn (split_decision)
                print ('\nYour total from Set #2 is', player_total)
                if (player_total > 21) and (player_total_split > 21):
                    dealer_play = "n"
                break
    else:
        player_total = player_turn (split_decision)

    if player_total < 22:
        print('\nYou stand, and Dealer starts its play.')


    # Dealer's turn to play
    dealer_total = dealer_turn (split_decision, dealer_play)

    # Start evalution and printing results

    if split_decision == "y":
        print ('\nResult of Set #1:')
        draw_line_message (banner = "")
        print ("Game Results:")
        drawing_history (player_split_pile)
        evaluate_result (player_total_split, dealer_total)
        print ('\nResult of Set #2:')

    # Processing Game Results

    draw_line_message (banner = "")
    print ("Game Results:")
    drawing_history (player_pile)
    evaluate_result (player_total, dealer_total)

def drawing_history (whose_turn):
    ''' Summary of cards drawn by player or dealer'''

    print ("Player cards:", end = " ")
    for cards in whose_turn:
        if cards[0] != 0:
            print (f'{card_suit[cards[0]]}{card_deck[cards[1]]}', end = " ")
    print ()

    print ("Dealer cards:", end = " ")
    for cards in dealer_pile:
        if cards[0] != 0:
            print (f'{card_suit[cards[0]]}{card_deck[cards[1]]}', end = " ")
    print()

def player_turn (split_decision):
    ''' Script to play Player side '''
    total = calculate_total (player_pile)

    if split_decision == "y":
        player_hit = dispense_card ("player")
        total = calculate_total (player_pile)

        print (f'\nHit! You draw a {card_suit[player_hit[0]]}{card_deck[player_hit[1]]}. \
    Your total is {total}.')
        split_decision = "n"

    while split_decision == "n":
        # checking whether player total >= 21 and get player input
        if total == 21:
            print ("\nThe chance is high for your winning. Let's see what dealer has.")
            player_decision = "s"
            time.sleep(2)
        elif total > 21:
            if player_pile[0][0] == 0 and player_pile[0][2] == 10:# to adjust value of Ace
                total -= 10
                player_pile.insert (0, (0,0,-10)) #position 0 in player_pile is for Ace indicator
                print (f'Adjusted the value of Ace. Your new total is {total}')
                continue
            print('        Busted. Total is greater than 21...')
            return total
        else:
            player_decision = input ('Hit or Stand, h/s? ').replace (" ", "") #remove space

        # Generating the next card when player hits
        if player_decision.lower() == "h":
            player_hit = dispense_card ("player")
            total = calculate_total (player_pile)
            if player_hit[1] == 1 and total < 12:
                total += 10
                player_pile.insert(0, (0,0,10))
            print (f'\nHit! You draw a {card_suit[player_hit[0]]}{card_deck[player_hit[1]]}. \
Your total is {total}.')

        elif player_decision.lower() == "s":
            return total

        else:
            print ('Please choose only h or s.')




def dealer_turn (split_decision, dealer_play):
    '''
    Created a function as states became too long in def play_black_jack
    Dealing processes after player choses Stay, or it's Dealer's turn

    '''
    # Case when both results of split play are Bursted, skip dealer dealer_turn
    # When player budted, there is no need to play dealer
     #set value for normal play
    player_total = calculate_total (player_pile)
    dealer_total = calculate_total (dealer_pile)

    if split_decision == "n":
        if player_total > 21:
            dealer_play = "n"


    if dealer_play != "n":
        print(f'\nDealer reveals the hidden card of \
{card_suit[dealer_pile[-1][0]]}{card_deck[dealer_pile[-1][1]]} and', end = " ")

    # check Blackjack and adjust value of face card

        if dealer_pile[0][0] == 0: # to check Balckjack
            if (dealer_pile[-2][1] > 10) or (dealer_pile[-1][1] > 10):
                print ('Dealer has Balckjack!!!')
                time.sleep(1)

        print(f'Dealer has a total of {dealer_total}.')
        time.sleep (1)

    while dealer_play == "y":


        # Loops for dealer's drawing
        while dealer_total < 17:
            dealer_hit = dispense_card ("dealer")
            dealer_total = calculate_total (dealer_pile)

            if dealer_hit[1] == 1 and dealer_total <12: #adjust value for Ace
                dealer_total += 10
                dealer_pile.insert (0, (0,0,10))
            print (f'\nDealer draws a \
{card_suit[dealer_hit[0]]}{card_deck[dealer_hit[1]]}.', end = " ")

            print(f'Dealer total is {dealer_total}')
            time.sleep (1)

            if dealer_total > 21:
                if dealer_pile[0][0] == 0 and dealer_pile[0][2] == 10: # adjust value for Ace
                    dealer_total -= 10
                    dealer_pile.insert (0, (0,0,-10))
                    print (f'Adjusted the value of Ace. Dealer new total is {dealer_total}.')
                    continue

                print('        Busted. Total is greater than 21...')
                dealer_play = "n"

        if dealer_total <22:
            print ('\nDealer stands.')
            break

    return dealer_total
        # Decide the winner when dealer total exceeds 16

def player_turn_split ():
    ''' Script to play Player split '''


    player_hit = dispense_card ("split")
    total = calculate_total (player_split_pile)

    print (f'\nHit! You draw a {card_suit[player_hit[0]]}{card_deck[player_hit[1]]}. \
Your total is {total}.')

    while True:
        # checking whether player total >= 21 and get player input
        if total == 21:
            print ("\nThe chance is high for your winning. Let's see what dealer has.")
            player_decision = "s"
            time.sleep(2)
        elif total > 21:
            if player_pile[0][0] == 0 and player_pile[0][2] == 10:# to adjust value of Ace
                total -=10
                player_split_pile.insert (0, (0,0,-10))
                print (f'Adjusted the value of Ace. Your new total is {total}')
                continue
            print('        Busted. Total is greater than 21...')
            return total
        else:
            player_decision = input ('Hit or Stand, h/s? ').replace(" ", "") #remove space

        # Generating the next card when player hits
        if player_decision.lower() == "h":
            player_hit = dispense_card ("split")
            total = calculate_total (player_split_pile)
            if player_hit[1] == 1 and total < 12:
                total +=10
                player_pile.insert(0, (0,0,10))
            print (f'\nHit! You draw a {card_suit[player_hit[0]]}{card_deck[player_hit[1]]}. \
Your total is {total}.')

        elif player_decision.lower() == "s":
            return total

        else:
            print ('Please choose only h or s.')


def evaluate_result (player_total, dealer_total):
    ''' Evaluate and print the result '''

    if dealer_total > 21:
        if player_total > 21:
            print ('\nYou busted.', end = " ")
            winner = "Dealer"
            print_result(winner, player_total, dealer_total)
            count_dealer_win.append(1)

        else:
            print ('\nDealer busted.', end = " ")
            winner = "You"
            print_result(winner, player_total, dealer_total)
            count_player_win.append(1)

    else:
        if player_total > 21:
            print ('You busted.')
            winner = "Dealer"
            print_result(winner, player_total, dealer_total)
            count_dealer_win.append(1)
        elif dealer_total > player_total:
            winner = "Dealer"
            print_result(winner, player_total, dealer_total)
            count_dealer_win.append(1)
        elif dealer_total == player_total:
            winner = "Nobody"
            print_result(winner, player_total, dealer_total)
            count_tie_score.append(1)
        else:
            winner = "You"
            print_result(winner, player_total, dealer_total)
            count_player_win.append(1)

    statistics() # statistics and display

def print_result (winner, player_total, dealer_total):
    '''
    To print the result.

    '''
    if player_total > 21 or dealer_total > 21:
        print (f'{winner} won!!')
        time.sleep (1)

    else:
        print (f'\n{winner} won!!', end = " ")
        print (f'Your total is {player_total} and dealer total is {dealer_total}.')
        time.sleep (1)

def statistics ():
    '''
    statistics of winnings
    '''
    number_dealer_win = sum(count_dealer_win)
    number_player_win = sum(count_player_win)
    total_wins = number_dealer_win + number_player_win
    number_tie_score =sum(count_tie_score)
    total_played = number_dealer_win + number_player_win + number_tie_score
    if total_wins != 0:
        winning_ratio = number_player_win / total_played
        winning_ratio2 = number_player_win / total_wins
        print ('\nsatistics:')
        print (f'You won {number_player_win} times : Dealer won {number_dealer_win} times:\
 Tie {number_tie_score} times.')
        print (f'Your winning ratio is {winning_ratio:.1%}.', end = " ")
        print (f'Excluding Ties, winning ratio is {winning_ratio2:.1%}')

        if winning_ratio > 0.6:
            print ('\nFantastic job! If you can keep the ratio over 60%, \
Casino will like neither you nor this program.\n')
        elif winning_ratio > 0.5:
            print ('\nWonderful job! You are beating the dealer!\n')
        elif winning_ratio >0.4:
            print ('\nGood job!. Maintaining the ratio over 40% is not easy.\n')
        else:
            print ('\nCan you beat the programing logic with the winning ratio over 40%?\n')


def draw_line_message (banner):
    '''
    To avoid repetition, created a simple functon to draw lines and message.
    '''
    print ('\n', "=" * 80, '\n')
    if banner:
        print (f'{banner:^80}')
        print ('\n', "=" * 80, '\n')

def welcome_sign ():
    '''
    Welcome message at the beginning of the game
    '''

    msg = ('''
    w           w eeeeeee  @            ccccc      ooo     mm        mm  eeeeeee
     ww       ww  @        @          cc         oo   oo   m mm    mm m  @
      ww  w  ww   @eeee    @          cc        oo     oo  m  mm  mm  m  @eeee
       w  w  w    @        @          cc         oo   oo   m    mm    m  @
        w   w     eeeeeee  @LLLLLLLL    ccccc      ooo     m          m  eeeeeee
    ''')

    for space in range (7, 0, -1):
        os.system('cls')
        print ('\n' * space)
        print (msg)
        time.sleep (0.1)

    draw_line_message (banner="Blackjack")


# Loop to ask player to play continually and calling a function accordingly
if __name__ == '__main__':
    main()
