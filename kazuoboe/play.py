import random
import sys

import tkinter
from tkinter.font import Font

from kazuoboe import games


class Interface(tkinter.Frame):
    def __init__(self, master):
        # windows and widgets
        super().__init__(master)
        self.root = master
        self.main_label = tkinter.Label(
            self.root,
            text="Welcome to Kazuoboe!",
            font=Font(family="Courier", size=24)
        )
        self.name_label_1 = tkinter.Label(
            self.root,
            text="Enter your name :)",
            font=Font(family="Courier", size=18)
        )
        self.name_label_2 = tkinter.Label(
            self.root,
            text="Enter your name :)",
            font=Font(family="Courier", size=18)
        )
        self.entry_1 = tkinter.Entry(self.root, width=10)
        self.entry_2 = tkinter.Entry(self.root, width=10)
        self.button = tkinter.Button(
            self.root,
            text="Start",
            width=10,
            font=Font(family="Courier", size=15)
        )
        self.input_from_player = None

    def configure(self):
        """ configure positions and sizes of widgets """
        self.root.title("kazuoboe")
        self.root.geometry("700x500")

        self.main_label.place(x=350, y=100, anchor="center")
        self.name_label_1.place(x=200, y=200, anchor="center")
        self.name_label_2.place(x=500, y=200, anchor="center")
        self.entry_1.place(x=200, y=250, anchor="center")
        self.entry_1.focus_set()
        self.entry_2.place(x=500, y=250, anchor="center")
        self.button.place(x=350, y=350, anchor="center")

        self.button.bind("<Button-1>", self.init_game)
        self.root.bind("<Return>", self.init_game)

    def init_game(self, event):
        self.button.bind("<Button-1>", self.get_new_number)
        self.root.bind("<Return>", self.get_new_number)
        self.button.config(text="OK")

        name_1, name_2 = self.entry_1.get(), self.entry_2.get()
        self.entry_1.delete(0, "end")
        self.entry_2.delete(0, "end")
        self.name_label_1.config(
            text=name_1,
            font=Font(family="Courier", size=24))
        self.name_label_2.config(
            text=name_2,
            font=Font(family="Courier", size=24))

        self.game = games.Kazuoboe(name_1, name_2)
        self.game.decide_order()

        self.set_focus_on_entry()
        self.game.generate_rand()
        self.main_label.config(
            text=f"{self.game.cur_player.name}のターンです！\n新しい数字を入力してください: {self.game.rand-4} ~ {self.game.rand+4}",
            font=Font(family="Helvetica", size=18),
        )

    def set_focus_on_entry(self):
        if self.game.cur_player == self.game.player_1:
            self.entry_1.focus_set()
        else:
            self.entry_2.focus_set()

    def get_new_number(self, event):
        if self.game.cur_player == self.game.player_1:
            input_1 = self.entry_1.get()
            self.entry_1.delete(0, "end")
            self.input_from_player = int(input_1)
        else:
            input_2 = self.entry_2.get()
            self.entry_2.delete(0, "end")
            self.input_from_player = int(input_2)

        # TODO: make it not freeze...
        if self.game.new_num_is_in_range(self.input_from_player, 4):
            self.main_label.config(
                text=f"範囲外です。もう一度入力してください: {self.game.rand-4} ~ {self.game.rand+4}\n",
                font=Font(family="Helvetica", size=18),
            )
            self.button.bind("<Button-1>", self.get_correct_new_number)
            self.root.bind("<Return>", self.get_correct_new_number)

        self.game.cur_player.numbers.append(self.input_from_player)

        self.game.choose_index_to_ask()
        self.main_label.config(
            text=f"{self.game.idx}番目に入力した数字はなんでしたか？\n",
            font=Font(family="Helvetica", size=18),
        )

        self.button.bind("<Button-1>", self.get_past_number)
        self.root.bind("<Return>", self.get_past_number)

    # 入力の範囲が誤っていた時にもう一度取得
    def get_correct_new_number(self, event):
        if self.game.cur_player == self.game.player_1:
            input_1 = self.entry_1.get()
            self.entry_1.delete(0, "end")
            self.input_from_player = int(input_1)
        else:
            input_2 = self.entry_2.get()
            self.entry_2.delete(0, "end")
            self.input_from_player = int(input_2)

    def get_past_number(self, event):
        if self.game.cur_player == self.game.player_1:
            input_1 = self.entry_1.get()
            self.entry_1.delete(0, "end")
            self.input_from_player = int(input_1)
        else:
            input_2 = self.entry_2.get()
            self.entry_2.delete(0, "end")
            self.input_from_player = int(input_2)

        true = self.game.cur_player.numbers[self.game.idx - 1]
        if self.input_from_player != true:
            self.main_label.config(
                text=f"{self.game.cur_player.name}の負けです:(\n\n正しい答えは{true}ですが、{self.game.cur_player.name}は{self.input_from_player}と答えました:(",
                font=Font(family="Helvetica", size=18),
            )
            self.game.done = True

        if self.game.done:
            # self.main_label.config(text=f"Finished!", font=Font(family="Courier", size=18))
            self.button.config(text="Exit", font=Font(family="Courier", size=15))
            self.button.bind("<Button-1>", self.exit)
        else:
            self.game.change_turn()
            self.set_focus_on_entry()
            self.ask_new_number()

    # windowを閉じる
    def exit(self, event):
        sys.exit()

    def ask_new_number(self):
        self.rand = int(random.uniform(0, 100))
        self.main_label.config(
            text=f"{self.game.cur_player.name}のターンです！\n新しい数字を入力してください: {self.rand-4} ~ {self.rand+4}",
            font=Font(family="Helvetica", size=18),
        )
        self.button.bind("<Button-1>", self.get_new_number)
        self.root.bind("<Return>", self.get_new_number)


if __name__ == "__main__":
    root = tkinter.Tk()
    interface = Interface(root)
    interface.configure()
    interface.mainloop()
