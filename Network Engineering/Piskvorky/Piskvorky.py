
import numpy as np

# Color codes
RED = '\x1b[31m'
GREEN = '\x1b[32m'
YELLOW = '\x1b[33m'
BLUE = '\x1b[34m'
MAGENTA = '\x1b[35m'
CYAN = '\x1b[36m'
RESET = '\x1b[0m'


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
            print(RED+"Nemôžeš ísť na toto políčko!"+RESET)
            return False

    def input_number(thread, Piskvorky):
        user_input = 0
        while not thread.stop_flag:
            try:
                if Piskvorky.suradnica == 'X':
                    user_input = int(input("Hráč "+Piskvorky.hrac+", zadaj suradnicu X: "))
                else:
                    user_input = int(input("Hráč "+Piskvorky.hrac+", zadaj suradnicu Y: "))
            except ValueError:
                print("Wrong value")
                continue
            if user_input >= 1 and user_input <= Piskvorky.velkost:
                break
            else:
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
                        print(GREEN+"Vyhral hráč " + Piskvorky.hrac+", pre ukončenie stlač ESC"+RESET)
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
                        print(GREEN+"Vyhral hráč " + Piskvorky.hrac+", pre ukončenie stlač ESC"+RESET)
                        return True
                else:
                    pocet = 0

    def check_diagonal(Piskvorky):
        #hlavna diagonala
        for i in range(Piskvorky.velkost - Piskvorky.pocet_vitaznych + 1):
            for j in range(Piskvorky.velkost - Piskvorky.pocet_vitaznych + 1):
                if Piskvorky.hraciaPlocha[i][j] == Piskvorky.hrac and Piskvorky.hraciaPlocha[i+1][j+1] == Piskvorky.hrac and Piskvorky.hraciaPlocha[i+2][j+2] == Piskvorky.hrac:
                    print(GREEN+"Vyhral hráč " + Piskvorky.hrac+", pre ukončenie stlač ESC"+RESET)
                    return True

        #vedlajsia diagonala
        for i in range(Piskvorky.velkost - Piskvorky.pocet_vitaznych + 1):
            for j in reversed(range(Piskvorky.velkost)):
                if Piskvorky.hraciaPlocha[i][j] == Piskvorky.hrac and Piskvorky.hraciaPlocha[i+1][j-1] == Piskvorky.hrac and Piskvorky.hraciaPlocha[i+2][j-2] == Piskvorky.hrac:
                    print(GREEN+"Vyhral hráč " + Piskvorky.hrac+", pre ukončenie stlač ESC"+RESET)
                    return True

    def check_win(Piskvorky):
        if Piskvorky.check_row() or Piskvorky.check_column() or Piskvorky.check_diagonal():
            return True

