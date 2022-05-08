import random


def different_cases(section_count):
    money = 100000
    bet = 100
    wins = 0
    losses = 0
    games = 0
    while money > 0 and games < 60000:
        if bet > money:
            bet = money
        money -= bet

        roll = random.randint(1, section_count)

        if roll in range(1, 19):
            money += bet * 2
            wins += 1
        else:
            losses += 1
        games = wins + losses
    print(f"Выиграно ставок: {wins}, Проиграно: {losses}, Всего сыграно игр: {games}")


if __name__ == '__main__':
    different_cases(37)
    different_cases(36)
    different_cases(35)