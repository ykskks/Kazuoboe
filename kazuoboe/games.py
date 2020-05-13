import random
import time


class Player:
    def __init__(self, name):
        self.name = name
        self.numbers = []

    def __eq__(self, other):
        return self.name == other

    def add(self, new_num):
        self.numbers.append(new_num)


class Kazuoboe:
    def __init__(self, name_1, name_2):
        self.player_1 = Player(name_1)
        self.player_2 = Player(name_2)
        self.is_player1_on_turn = True
        self.cur_player = self.player_1
        self.done = False
        self.seed = int(time.time())
        random.seed(self.seed)
        self.rand = None
        self.idx = None

    def decide_order(self):
        """ decide order for the game randomly"""
        if random.uniform(0, 1) < 0.5:
            self.is_player1_on_turn = False
            self.cur_player = self.player_2

    def change_turn(self):
        """ change current player to proceed to next turn """
        self.is_player1_on_turn = not self.is_player1_on_turn
        self.cur_player = self.player_1 if self.is_player1_on_turn else self.player_2

    def generate_rand(self, start=0, end=100):
        self.rand = int(random.uniform(start, end))

    def new_num_is_in_range(self, new_num, ok_range):
        """ judge if the user input number is in the appropriate range """
        return self.rand - ok_range <= new_num <= self.rand + ok_range

    def choose_index_to_ask(self):
        self.idx = random.choice(range(1, len(self.cur_player.numbers) + 1))

    def add_new_num(self, new_num):
        self.cur_player.add(new_num)

    def ans_is_correct(self, ans):
        return ans == self.cur_player.numbers[self.idx]

    def interactive(self):
        print("Interactive mode (Not implemented.)")


if __name__ == "__main__":
    name_1 = input("Player1, name: \n")
    name_2 = input("Player2, name:\n")
    game = Kazuoboe(name_1, name_2)
    game.interactive()
