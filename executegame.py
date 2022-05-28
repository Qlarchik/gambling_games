from pathlib import Path

if __name__ == '__main__':
    while True:
        print("Games: \n roulette \n craps \n slotmachine \n baccarat")
        game = input("Enter game name: ")
        try:
            exec(Path("games/" + game.lower() + ".py").read_text())
            break
        except FileNotFoundError as e:
            print("File doesn't exist, try again")
            continue
