import random
import sys
import time
import tkinter
from tkinter.font import Font


class Player:
    def __init__(self, name):
        self.name = name
        self.numbers = []

    def __eq__(self, other):
        return self.name == other


class MyGame:
    def __init__(
        self, main_label, name_label_1, name_label_2, entry_1, entry_2, button
    ):
        self.main_label = main_label
        self.name_label_1 = name_label_1
        self.name_label_2 = name_label_2
        self.entry_1 = entry_1
        self.entry_2 = entry_2
        self.button = button

        self.idx = None
        self.rand = None
        self.done = False
        self.seed = int(time.time())
        random.seed(self.seed)

    # playerの名前をentryから取得, それを元にplayerをインスタンス化
    def get_names(self):
        self.button.bind(
            "<Button-1>", self.get_new_number
        )  # 以後はボタンを押すとget_new_numberが呼ばれる
        root.bind("<Return>", self.get_new_number)
        self.button.config(text="OK")
        name_1, name_2 = self.entry_1.get(), self.entry_2.get()
        self.entry_1.delete(0, "end")
        self.entry_2.delete(0, "end")
        self.name_label_1.config(text=name_1, font=Font(family="Courier", size=24))
        self.name_label_2.config(text=name_2, font=Font(family="Courier", size=24))
        self.player_1 = Player(name_1)
        self.player_2 = Player(name_2)
        self.players = [self.player_1, self.player_2]
        self.cur_player = None
        self.input_from_player = None

    # どっちのentryに名前を書いても順番がランダムになるように
    def decide_order(self):
        if random.uniform(0, 1) < 0.5:
            self.players = [self.player_2, self.player_1]
        self.cur_player = self.players[0]

    # 新たな数字の入力を促す
    def ask_new_number(self):
        self.rand = int(random.uniform(0, 100))
        self.main_label.config(
            text=f"{self.cur_player.name}のターンです！\n新しい数字を入力してください: {self.rand-4} ~ {self.rand+4}",
            font=Font(family="Helvetica", size=18),
        )
        self.button.bind("<Button-1>", self.get_new_number)
        root.bind("<Return>", self.get_new_number)

    # 入力の範囲が誤っていた時にもう一度取得
    def get_correct_new_number(self, event):
        if self.cur_player == self.player_1:
            input_1 = entry_1.get()
            self.entry_1.delete(0, "end")
            self.input_from_player = int(input_1)
        else:
            input_2 = entry_2.get()
            self.entry_2.delete(0, "end")
            self.input_from_player = int(input_2)

    # 新たに入力された数字を取得する
    def get_new_number(self, event):
        if self.cur_player == self.player_1:
            input_1 = entry_1.get()
            self.entry_1.delete(0, "end")
            self.input_from_player = int(input_1)
        else:
            input_2 = entry_2.get()
            self.entry_2.delete(0, "end")
            self.input_from_player = int(input_2)

        # TODO: make it not freeze...
        if (
            self.input_from_player < self.rand - 4
            or self.rand + 4 < self.input_from_player
        ):
            self.main_label.config(
                text=f"範囲外です。もう一度入力してください: {self.rand-4} ~ {self.rand+4}\n",
                font=Font(family="Helvetica", size=18),
            )
            self.button.bind("<Button-1>", self.get_correct_new_number)
            root.bind("<Return>", self.get_correct_new_number)

        self.cur_player.numbers.append(self.input_from_player)

        self.idx = random.choice(range(1, len(self.cur_player.numbers) + 1))
        self.main_label.config(
            text=f"{self.idx}番目に入力した数字はなんでしたか？\n",
            font=Font(family="Helvetica", size=18),
        )

        self.button.bind("<Button-1>", self.get_past_number)
        root.bind("<Return>", self.get_past_number)

    # 過去の数字に関する質問の答えを取得し、勝ち負け判断。
    # 決まらなければ、次のplayerに新たな数字を聞く。以下繰り返し。
    def get_past_number(self, event):
        if self.cur_player == self.player_1:
            input_1 = entry_1.get()
            self.entry_1.delete(0, "end")
            self.input_from_player = int(input_1)
        else:
            input_2 = entry_2.get()
            self.entry_2.delete(0, "end")
            self.input_from_player = int(input_2)

        true = self.cur_player.numbers[self.idx - 1]
        if self.input_from_player != true:
            self.main_label.config(
                text=f"{self.cur_player.name}の負けです:(\n\n正しい答えは{true}ですが、{self.cur_player.name}は{self.input_from_player}と答えました:(",
                font=Font(family="Helvetica", size=18),
            )
            self.done = True

        if self.done:
            # self.main_label.config(text=f"Finished!", font=Font(family="Courier", size=18))
            self.button.config(text="Exit", font=Font(family="Courier", size=15))
            self.button.bind("<Button-1>", self.exit)
        else:

            self.cur_player = [
                self.player
                for self.player in self.players
                if self.player != self.cur_player
            ][0]
            self.set_focus_on_entry()
            self.ask_new_number()

    # windowを閉じる
    def exit(self, event):
        sys.exit()

    # 回答を求めるプレイヤーのentryにファーカスを当てる
    def set_focus_on_entry(self):
        if self.cur_player == self.player_1:
            entry_1.focus_set()
        else:
            entry_2.focus_set()

    def main(self, event):
        self.get_names()
        self.decide_order()

        self.set_focus_on_entry()
        self.rand = int(random.uniform(0, 100))
        self.main_label.config(
            text=f"{self.cur_player.name}のターンです！\n新しい数字を入力してください: {self.rand-4} ~ {self.rand+4}",
            font=Font(family="Helvetica", size=18),
        )


if __name__ == "__main__":
    # 箱を用意
    root = tkinter.Tk()
    root.title("kazuoboe")
    root.geometry("700x500")

    # 各widgetを用意
    main_label = tkinter.Label(
        root, text="Welcome to Kazuoboe!", font=Font(family="Courier", size=24)
    )
    main_label.place(x=350, y=100, anchor="center")

    name_label_1 = tkinter.Label(
        root, text="Enter your name :)", font=Font(family="Courier", size=18)
    )
    name_label_1.place(x=200, y=200, anchor="center")

    name_label_2 = tkinter.Label(
        root, text="Enter your name :)", font=Font(family="Courier", size=18)
    )
    name_label_2.place(x=500, y=200, anchor="center")

    entry_1 = tkinter.Entry(root, width=10)
    entry_1.place(x=200, y=250, anchor="center")
    entry_1.focus_set()

    entry_2 = tkinter.Entry(root, width=10)
    entry_2.place(x=500, y=250, anchor="center")

    button = tkinter.Button(
        root, text="Start", width=10, font=Font(family="Courier", size=15)
    )
    button.place(x=350, y=350, anchor="center")

    # widgetを持ったgameインスタンスを作成
    mygame = MyGame(main_label, name_label_1, name_label_2, entry_1, entry_2, button)

    # startボタンが押されたらgameインスタンスのmain()が呼ばれて開始
    button.bind("<Button-1>", mygame.main)
    root.bind("<Return>", mygame.main)
    root.mainloop()
