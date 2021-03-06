import random
from art import *
from matplotlib import pyplot as plt


def check_combo(num1, num2, num3):
    if num1 == 1 and num2 == 1 and num3 == 1:
        return 2
    elif num1 == 1 and num2 == 1 and num3 != 1:
        return 0
    elif num1 == 2 and num2 == 2 and num3 != 2:
        return 0
    elif num1 == 3 and num2 == 3 and num3 == 3:
        return 14
    elif num1 == 4 and num2 == 4 and num3 == 4:
        return 29
    else:
        return -1


if __name__ == '__main__':
    Art = text2art("Slot machine")
    print(Art)

    reel1 = [1, 2, 3, 4]
    reel2 = [2, 2, 1, 3, 4]
    reel3 = [4, 3, 1]
    balance = 60000
    bet = 1
    money = []

    for i in range(0, 60000):
        r1 = random.randrange(0, len(reel1))
        r2 = random.randrange(0, len(reel2))
        r3 = random.randrange(0, len(reel3))
        first_num = reel1[r1]
        second_num = reel2[r2]
        third_num = reel3[r3]

        multiplication = check_combo(first_num, second_num, third_num)
        balance += bet * multiplication
        money.append(balance)

        print(f">>> {first_num} - {second_num} - {third_num} <<< \n Your x: {multiplication} \n Balance: {balance}")

    RTP = round(balance / 60000 * 100, 1)
    print(f"Balance: {balance} RTP {RTP}")

    plt.plot(money)
    plt.show()
