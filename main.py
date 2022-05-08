import random


def first_case():
    money = 100000
    bet = 100
    wins = 0
    losses = 0
    games = 0
    while money > 0:
        if bet > money:
            bet = money
        money -= bet

        roll = random.randint(1, 37)

        if roll in range(1, 19):
            money += bet * 2
            wins += 1
        else:
            losses += 1
        games = wins + losses
    print(f"Выиграно ставок: {wins}, Проиграно: {losses}, Всего сыграно игр: {games}")


if __name__ == '__main__':
    first_case()
