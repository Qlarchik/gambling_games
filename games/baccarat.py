import random
import math
import sys
from art import *

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


def deck_generator():
    d = {}
    for suit in suits:
        for card, val in cardValues.items():
            d[f'{card} of {suit}'] = val
    return d


# Draw function
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


bets = {
    "Player": 0,
    "Banker": 0,
    "Tie": 0
}


def bet_prompt():
    global bank
    while True:
        try:
            bet = int(input("\t$> "))
        except ValueError:
            print("\tThat wasn't a number!")
            continue
        if bet > bank:
            print("\tNot enough money. Do you want to add more to your balance?")
            add_more = input(">")
            if add_more.lower() in ['y', 'yes', 'atm', 'help', 'more money']:
                out_of_money()
            continue
        elif bet <= 0:
            print("You have to make a bet to play!")
            continue
        else:
            return bet


def out_of_money():
    global bank
    if bank <= 0:
        print("\tYou are totally out of money. Let's hit the ATM again and get you more cash. How much do you want?")
    else:
        print("\tYour chips are getting really low. How much would you like to add to your bankroll?")
    while True:
        try:
            cash = int(input("\t$>"))
        except ValueError:
            print("\tYou forgot what numbers were and the ATM beeps at you in annoyance. Try again.")
            continue
        if cash <= 0:
            print("\tWhat am I, a bank? This is for withdrawals only! Try again.")
            continue
        else:
            bank += cash
            break
    print(f"\tAlright, starting you off again with {bank}. Don't lose it all this time!")


def player_bet():
    global bets, decisions
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
            print(f"Decision Table for the current game:\n{decisions}")
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


def vig(bet):
    total = bet * 0.05
    if bet < 25:
        commission = math.ceil(total)
    else:
        commission = math.floor(total)
    print(f"${commission} paid to the House for the vig.")
    return commission


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
            bank -= vig(bets["Banker"])
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
    global playerHand, bankerHand, decisions, bank
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
    if len(decisions) <= 10:
        decisions.append(outcome.upper())
    else:
        decisions.pop(0)
        decisions.append(outcome.upper())

    # Payout and Side Bets
    payout(outcome)


decisions = []


def burn():
    i = 0
    for i in range(10):
        draw()
        i += 1
    print("\n\tBurning 10 Cards!\n")


# Game start
if __name__ == '__main__':
    Art = text2art("Baccarat")
    print(Art)

    deck = deck_generator()
    print("\n\tShuffling the Deck!\n")
    burn()

    print("Enter your deposit")
    while True:
        try:
            bank = int(input("$"))
            break
        except ValueError:
            print("That wasn't a number")
            continue
    print(f"Great, starting off with {bank}. Good luck!")

    playerHand = 0
    bankerHand = 0

    while True:

        if bank <= 0:
            out_of_money()

        if len(deck) <= 10:
            deck = deck_generator()
            del discard[:]
            print("\nShuffling the Deck!\n")
            burn()
            decisions = []
            print(discard)
        # Betting
        print("Place your bets!")
        player_bet()

        # Drawing hands
        baccarat()
        print(f"You now have ${bank} in your bank.\n\n")
        # input("Hit Enter for the next hand...")
        continue
