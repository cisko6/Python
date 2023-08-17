
import numpy as np
import keyboard, threading, sys

done = False

class Piskvorky:
    def __init__(self, velkost, hrac, suradnica, pocet_vitaznych):
        self.velkost = velkost
        self.hraciaPlocha = np.zeros((velkost, velkost), dtype='U1')
        self.hrac = hrac
        self.suradnica = suradnica
        self.pocet_vitaznych = pocet_vitaznych


def vytlac_plochu(Piskvorky):
    for riadok in Piskvorky.hraciaPlocha:
        print("\n|", end="")
        for policko in riadok:
            if policko == '':
                print(' ', end='')
            else:
                print(policko, end='')
            print("|", end="")
    print("\n")


def make_move(Piskvorky, riadok, stlpec):
    if Piskvorky.hraciaPlocha[riadok][stlpec] == '' and (Piskvorky.hrac == 'X' or Piskvorky.hrac == 'O'):
        Piskvorky.hraciaPlocha[riadok][stlpec] = Piskvorky.hrac
        return True
    else:
        print("Nemôžeš ísť na toto políčko!")
        return False


def input_number(Piskvorky):
    user_input = 0
    global done
    while not done:
        try:
            if Piskvorky.suradnica == 'X':
                user_input = int(input("Hráč "+Piskvorky.hrac+", zadaj suradnicu X: "))
            else:
                user_input = int(input("Hráč "+Piskvorky.hrac+", zadaj suradnicu Y: "))
        except ValueError:
            if done == False:
                print("Wrong value")
            continue
        if user_input >= 1 and user_input <= Piskvorky.velkost:
            break
        else:
            if done == False:
                print("Wrong number!")
    return user_input

def vymen_strany(Piskvorky):
    if Piskvorky.hrac == 'X':
        Piskvorky.hrac = 'O'
    else:
        Piskvorky.hrac = 'X'


def check_row(Piskvorky):
    for riadok in Piskvorky.hraciaPlocha:
        pocet = 0
        for policko in riadok:
            if policko == Piskvorky.hrac:
                pocet += 1
                if pocet == Piskvorky.pocet_vitaznych:
                    print("Vyhral hráč " + Piskvorky.hrac+", pre ukončenie stlač ESC")
                    return True
            else:
                pocet = 0


def check_column(Piskvorky):
    for stlpec in zip(*Piskvorky.hraciaPlocha):
        pocet = 0
        for policko in stlpec:
            if policko == Piskvorky.hrac:
                pocet += 1
                if pocet == Piskvorky.pocet_vitaznych:
                    print("Vyhral hráč " + Piskvorky.hrac+", pre ukončenie stlač ESC")
                    return True
            else:
                pocet = 0


def check_diagonal(Piskvorky):
    #hlavna diagonala
    for i in range(Piskvorky.velkost - Piskvorky.pocet_vitaznych + 1):
        for j in range(Piskvorky.velkost - Piskvorky.pocet_vitaznych + 1):
            if Piskvorky.hraciaPlocha[i][j] == Piskvorky.hrac and Piskvorky.hraciaPlocha[i+1][j+1] == Piskvorky.hrac and Piskvorky.hraciaPlocha[i+2][j+2] == Piskvorky.hrac:
                print("Vyhral hráč " + Piskvorky.hrac+", pre ukončenie stlač ESC")
                return True

    #vedlajsia diagonala
    for i in range(Piskvorky.velkost - Piskvorky.pocet_vitaznych + 1):
        for j in reversed(range(Piskvorky.velkost)):
            if Piskvorky.hraciaPlocha[i][j] == Piskvorky.hrac and Piskvorky.hraciaPlocha[i+1][j-1] == Piskvorky.hrac and Piskvorky.hraciaPlocha[i+2][j-2] == Piskvorky.hrac:
                print("Vyhral hráč " + Piskvorky.hrac+", pre ukončenie stlač ESC")
                return True


def check_win(Piskvorky):
    if check_row(Piskvorky) or check_column(Piskvorky) or check_diagonal(Piskvorky):
        return True


def run_game(Piskvorky):
    vytlac_plochu(Piskvorky)
    global done
    while not done:
            user_input1 = input_number(Piskvorky)
            Piskvorky.suradnica = 'Y'
            user_input2 = input_number(Piskvorky)
            Piskvorky.suradnica = 'X'

            if pisk.hrac == 'X':
                make_move(Piskvorky, user_input1 - 1, user_input2 - 1)
            else:
                make_move(Piskvorky, user_input1 - 1, user_input2 - 1)
            vytlac_plochu(Piskvorky)
            if check_win(Piskvorky):
                done = True
            vymen_strany(Piskvorky)
    sys.exit()


def stop_game(e):
    if e.name == 'esc':
        global done
        print("\nGame Stopped")
        done = True

while True:
    try:
        velkost = int(input("Zadaj velkost poľa: "))
        if velkost < 3:
            print("Musíš zadať číslo minimálne rovné trom!")
        if isinstance(velkost,int) and velkost >= 3:
            break
    except ValueError:
        print("Musíš zadať číslo!")

while True:
    hrac = input("Ktorý hráč by mal začínať? (X,O): ")
    if hrac == 'X' or hrac == 'O':
        break
    else:
        print("Musíš zadať buď len X alebo O!")

while True:
    try:
        pocet_vitaznych = int(input("Na koľko víťazných by sa malo hrať? "))
        if pocet_vitaznych <= velkost:
            break
        else:
            print("Nemože sa hrať na viac víťažných ako je veľkosť poľa")
    except ValueError:
        print("Musíš zadať číslo!")

pisk = Piskvorky(velkost, hrac, 'X', pocet_vitaznych)

thread = threading.Thread(target=run_game, args=(pisk, ),daemon=True)
thread.start()

keyboard.on_press(stop_game)
keyboard.wait('esc')

exit()
