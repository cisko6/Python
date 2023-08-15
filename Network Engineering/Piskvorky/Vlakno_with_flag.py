
import Piskvorky, threading


class MyThread(threading.Thread):
    def __init__(self, Piskvorky):
        super().__init__()
        self.stop_flag = False
        self.Piskvorky = Piskvorky

    def run(self):
        Piskvorky.Piskvorky.vytlac_plochu(self.Piskvorky)
        while not self.stop_flag:  # This is the line we're explaining
            user_input1 = Piskvorky.Piskvorky.input_number(self,self.Piskvorky)
            self.Piskvorky.suradnica = 'Y'
            user_input2 = Piskvorky.Piskvorky.input_number(self,self.Piskvorky)
            self.Piskvorky.suradnica = 'X'

            if self.stop_flag:
                break

            if self.Piskvorky.hrac == 'X':
                Piskvorky.Piskvorky.make_move(self.Piskvorky, user_input1 - 1, user_input2 - 1)
            else:
                Piskvorky.Piskvorky.make_move(self.Piskvorky, user_input1 - 1, user_input2 - 1)
            Piskvorky.Piskvorky.vytlac_plochu(self.Piskvorky)
            if Piskvorky.Piskvorky.check_win(self.Piskvorky):
                self.stop_flag = True
            Piskvorky.Piskvorky.vymen_strany(self.Piskvorky)
        exit()

    def stop(self):
        self.stop_flag = True


def stop_game(e,thread):
    if e.name == 'esc':
        print("\nGame Stopped")
        thread.stop_flag = True