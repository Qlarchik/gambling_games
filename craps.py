import random
from art import *
from matplotlib import pyplot as plt


def shoot():
    return random.randint(1, 6) + random.randint(1, 6)


def move():
    while True:
        val = shoot()
        if val == 7 or val == 11:
            return True
        if val == 2 or val == 3 or val == 12:
            return False


if __name__ == '__main__':
    Art = text2art("Craps")
    print(Art)
    money_total = 100
    win = 0
    loss = 0
    for p in range(100):
        bet = 1
        step = move()
        if step is True:
            money_total += bet
            win += 1
        else:
            money_total -= bet
            loss += 1
    print("Win", win, "Loss", loss, "Money", money_total)

    y = [shoot() for v in range(100)]
    plt.hist(y)
    plt.show()
