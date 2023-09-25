
import Piskvorky, Vlakno_with_flag, keyboard

RED = '\x1b[31m'
GREEN = '\x1b[32m'
YELLOW = '\x1b[33m'
BLUE = '\x1b[34m'
MAGENTA = '\x1b[35m'
CYAN = '\x1b[36m'
RESET = '\x1b[0m'


def main():
    while True:
        try:
            velkost = int(input("Zadaj velkost poľa: "))
            if velkost < 3:
                print(RED+"Musíš zadať číslo minimálne rovné trom!"+RESET)
            if isinstance(velkost,int) and velkost >= 3:
                break
        except ValueError:
            print(RED+"Musíš zadať číslo!"+RESET)

    while True:
        hrac = input("Ktorý hráč by mal začínať? (X,O): ")
        if hrac == 'X' or hrac == 'O':
            break
        else:
            print(RED+"Musíš zadať buď len X alebo O!"+RESET)

    while True:
        try:
            pocet_vitaznych = int(input("Na koľko víťazných by sa malo hrať? "))
            if pocet_vitaznych < 3:
                print(RED + "Nemože byť počet víťazných menší ako 3!" + RESET)
                continue
            if pocet_vitaznych <= velkost:
                break
            else:
                print(RED+"Nemože sa hrať na viac víťažných ako je veľkosť poľa"+RESET)
        except ValueError:
            print(RED+"Musíš zadať číslo!"+RESET)

    pisk = Piskvorky.Piskvorky(velkost, hrac, 'X', pocet_vitaznych)

    thread = Vlakno_with_flag.MyThread(pisk)
    thread.start()

    stop_game_partial = lambda e: Vlakno_with_flag.stop_game(e, thread)
    keyboard.on_press(stop_game_partial)
    keyboard.wait('esc')
    exit()

if __name__ == "__main__":
    main()
