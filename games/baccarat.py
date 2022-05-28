import random
import math
import sys
from art import *


def deck_generator():
    d = {}
    for suit in suits:
        for card, val in cardValues.items():
            d[f'{card} of {suit}'] = val
    return d


def draw():
    global deck, discard
    while True:
        card, card_val = random.choice(list(deck.items()))
        if discard.count(card) == 8:
            del deck[card]
            continue
        else:
            discard.append(card)
            break
    return card, card_val


def bet_prompt():
    global bank
    while True:
        try:
            bet = int(input("\t$> "))
        except ValueError:
            print("\tThat wasn't a number!")
            continue
        if bet > bank:
            print("This is a lot for you, try again")
            continue
        elif bet <= 0:
            print("You have to make a bet to play!")
            continue
        else:
            return bet


def player_bet():
    global bets, bet_decisions
    while True:
        for key in bets:
            if bets[key] > 0:
                print(f"You have ${bets[key]} on the {key} bet.")
        print("p - Player, b - Banker, t - Tie; Type 'x' to finish betting; Type 'exit' to terminate")
        choice = input("> ")
        if choice == 'p':
            print("How much on the Player Bet?")
            bets["Player"] = bet_prompt()
            print("Ok, ${} on the Player Bet.".format(bets["Player"]))
            continue
        elif choice == 'b':
            print("How much on the Banker Bet?")
            bets["Banker"] = bet_prompt()
            print("Ok, ${} on the Banker Bet.".format(bets["Banker"]))
            continue
        elif choice == 't':
            print("How much for the Tie Bet?")
            bets["Tie"] = bet_prompt()
            print("Ok, ${} on the Tie.".format(bets["Tie"]))
            continue
        elif choice == 'z':
            print("Zeroing out your bets.")
            for key in bets:
                bets[key] = 0
            continue
        elif choice == 'd':
            print(f"Decision Table for the current game:\n{bet_decisions}")
            continue
        elif choice == 'x':
            if bets["Tie"] > 0 or bets["Player"] > 0 or bets["Banker"] > 0:
                print("Done Betting! Drawing cards...")
                break
            else:
                print("Burning a hand with no bets. What fun!")
            break
        elif choice == 'exit':
            print("Script terminated")
            sys.exit()
        else:
            print("That's not a choice! Try again!")
            continue


def payout(outcome):
    global bets, bank
    if outcome == 'p':
        if bets["Player"] > 0:
            print("You win ${}!".format(bets["Player"]))
            bank += bets["Player"]
            bets["Player"] = 0
        if bets["Banker"] > 0:
            print("You lose ${}.".format(bets["Banker"]))
            bank -= bets["Banker"]
            bets["Banker"] = 0
        if bets["Tie"] > 0:
            print("You lose ${} from the Tie Bet.".format(bets["Tie"]))
            bank -= bets["Tie"]
            bets["Tie"] = 0
    elif outcome == 'b':
        if bets["Player"] > 0:
            print("You lose ${}.".format(bets["Player"]))
            bank -= bets["Player"]
            bets["Player"] = 0
        if bets["Banker"] > 0:
            print("You won ${}!".format(bets["Banker"]))
            bank += bets["Banker"]
            commission = math.floor(bets["Banker"] * 0.05)
            bank -= commission
            print(f"$You paid {commission} commission")
            bets["Banker"] = 0
        if bets["Tie"] > 0:
            print("You lost ${} from the Tie Bet.".format(bets["Tie"]))
            bank -= bets["Tie"]
            bets["Tie"] = 0
    elif outcome == 't':
        print("Player and Banker bets Push!")
        if bets["Tie"] > 0:
            print("You won ${} on the Tie Bet! Woo!".format(bets["Tie"] * 8))
            bank += bets["Tie"] * 8
        for key in bets:
            bets[key] = 0


def baccarat():
    global playerHand, bankerHand, bet_decisions, bank
    outcome = ''
    pHand = []
    bHand = []
    p3card = b3card = ''
    p3val = b3val = 0
    p1card, p1val = draw()
    pHand.append(p1val)
    b1card, b1val = draw()
    bHand.append(b1val)
    p2card, p2val = draw()
    pHand.append(p2val)
    b2card, b2val = draw()
    bHand.append(b2val)
    if p1val + p2val >= 10:
        playerHand = p1val + p2val - 10
    else:
        playerHand = p1val + p2val
    if b1val + b2val >= 10:
        bankerHand = b1val + b2val - 10
    else:
        bankerHand = b1val + b2val

    print("Player draws {p1} and {p2} for a total of {amount}.".format(p1=p1card, p2=p2card, amount=playerHand))
    print("Banker draws {b1} and {b2} for a total of {amount}.".format(b1=b1card, b2=b2card, amount=bankerHand))

    if playerHand == 9 and bankerHand == 9 or playerHand == 8 and bankerHand == 8:
        print("We have a Natural Tie!")
        outcome = 't'
    elif playerHand in [8, 9] and bankerHand < playerHand:
        print(f"Player wins with a Natural {playerHand}!")
        outcome = 'p'
    elif bankerHand in [8, 9] and playerHand < bankerHand:
        print(f"Banker Wins with a Natural {bankerHand}!")
        outcome = 'b'
    elif playerHand in [6, 7]:
        print(f"Player stands on {playerHand}.")
        if bankerHand == 7 and playerHand == 7:
            print("We have a Tie!")
            outcome = 't'
        elif bankerHand == 7 and playerHand == 6:
            print("Banker Wins!")
            outcome = 'b'
        elif bankerHand == 6 and playerHand == 7:
            print("Player Wins!")
            outcome = 'p'
        elif bankerHand > 7:
            print("Banker Wins!")
            outcome = 'b'
        else:
            b3card, b3val = draw()
            bHand.append(b3val)
            if bankerHand + b3val >= 10:
                bankerHand += b3val - 10
            else:
                bankerHand += b3val
            print("Banker draws {card} for a total of {amount}.".format(card=b3card, amount=bankerHand))
            if bankerHand == playerHand:
                print("We have a Tie!")
                outcome = 't'
            elif bankerHand < playerHand:
                print("Player Wins!")
                outcome = 'p'
            elif bankerHand > playerHand:
                print("Banker Wins!")
                outcome = 'b'
    else:
        p3card, p3val = draw()
        pHand.append(p3val)
        if playerHand + p3val >= 10:
            playerHand += p3val - 10
        else:
            playerHand += p3val
        print("Player draws {card} and now has {amount}.".format(card=p3card, amount=playerHand))
        if p3val in [2, 3] and bankerHand in range(5) or p3val in [4, 5] and bankerHand in range(6) or p3val in [6,
                                                                                                                 7] and bankerHand in range(
            7) \
                or p3val == 8 and bankerHand in range(3) or p3val in [0, 1, 9] and bankerHand in range(4):
            b3card, b3val = draw()
            bHand.append(b3val)
            if bankerHand + b3val >= 10:
                bankerHand += b3val - 10
            else:
                bankerHand += b3val
            print("Banker draws {card} for a total of {amount}.".format(card=b3card, amount=bankerHand))
        else:
            print(f"Banker stands with {bankerHand}.")
        if bankerHand == playerHand:
            print("We have a Tie!")
            outcome = 't'
        elif bankerHand < playerHand:
            print("Player Wins!")
            outcome = 'p'
        elif bankerHand > playerHand:
            print("Banker Wins!")
            outcome = 'b'
    if len(bet_decisions) <= 10:
        bet_decisions.append(outcome.upper())
    else:
        bet_decisions.pop(0)
        bet_decisions.append(outcome.upper())

    payout(outcome)


if __name__ == '__main__':
    Art = text2art("Baccarat")
    print(Art)

    deck = {}
    discard = []

    suits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']

    cardValues = {
        'Ace': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 0,
        'Jack': 0,
        'Queen': 0,
        'King': 0
    }

    bets = {
        "Player": 0,
        "Banker": 0,
        "Tie": 0
    }

    playerHand = 0
    bankerHand = 0

    bet_decisions = []

    deck = deck_generator()
    print("\n\tShuffling the Deck!\n")

    print("Enter your deposit")
    while True:
        try:
            bank = int(input("$"))
        except ValueError:
            print("That wasn't a number")
            continue
        if bank <= 0:
            print("Try again, but now enter a positive number")
            continue
        else:
            break
    print(f"Great, starting off with {bank}. Good luck!")

    while True:

        if bank <= 0:
            print("You lost all your money, bye!")
            sys.exit()

        if len(deck) <= 10:
            deck = deck_generator()
            del discard[:]
            print("\nRefreshing deck...\n")
            bet_decisions = []
            print(discard)
        # Betting
        print("Place your bets!")
        player_bet()

        # Drawing hands
        baccarat()
        print(f"You now have ${bank} in your bank.\n\n")
        continue
