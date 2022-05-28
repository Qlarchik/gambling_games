import random
from art import *
from matplotlib import pyplot as plt


def shoot():
    return random.randint(1, 6) + random.randint(1, 6)


def move():
    point = 0
    while True:
        val = shoot()
        if point == 0:
            if val == 7 or val == 11:
                return True
            if val == 2 or val == 3 or val == 12:
                return False
            point = val
        else:
            if val == 7:
                return False
            if val == point:
                return True


if __name__ == '__main__':
    Art = text2art("Craps")
    print(Art)

    money_total = 100
    win = 0
    loss = 0
    money = []
    while money_total > 0 and win + loss < 20000:
        money.append(money_total)
        bet = 1
        step = move()
        if step is True:
            money_total += bet
            win += 1
        else:
            money_total -= bet
            loss += 1
    print("Win", win, "Loss", loss, "Money", money_total, "Percentage", round(win/(win+loss)*100, 1))

    plt.plot(money)
    plt.show()
