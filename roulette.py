import random
from art import *
from plotly import graph_objs as go


def different_cases(section_count):
    list1 = []
    list2 = []
    money = 100000
    bet = 100
    wins = 0
    losses = 0
    games = 0
    while money > 0 and games < 100000:
        if bet > money:
            bet = money
        money -= bet

        list1.append(money)
        list2.append(len(list2) + 1)

        roll = random.randint(1, section_count)

        if roll in range(1, 19):
            money += bet * 2
            wins += 1
        else:
            losses += 1
        games = wins + losses
    percentage = round(wins / games * 100, 1)
    print(f"Выиграно ставок: {wins} Проиграно: {losses} Всего сыграно игр: {games} Процент побед: {percentage}%")
    return list1, list2


if __name__ == '__main__':
    Art = text2art("Roulette")
    print(Art)

    case1 = different_cases(37)
    case2 = different_cases(36)
    case3 = different_cases(35)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=case1[1], y=case1[0], name="Отрицательное матожидание"))
    fig.add_trace(go.Scatter(x=case2[1], y=case2[0], name="Нулевое матожидание"))
    fig.add_trace(go.Scatter(x=case3[1], y=case3[0], name="Положительное матожидание"))
    fig.show()