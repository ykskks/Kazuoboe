from kazuoboe.games import Player, Kazuoboe
import copy


# TODO: Use pytest fixture to setup/teardown
class TestPlayer:
    def test_eq_01(self):
        p1 = Player("sara")
        p2 = Player("sara")
        assert p1 == p2

    def test_eq_02(self):
        p1 = Player("sara")
        p2 = Player("martin")
        assert p1 != p2

    def test_add_01(self):
        p = Player("sara")
        p.add(3)
        assert p.numbers == [3]

    def test_add_02(self):
        p = Player("sara")
        assert p.numbers == []


# TODO: Use pytest fixture to setup/teardown
# TODO: Learn mock: Usage below correct?
class TestKazuoboe:
    def test_decide_order_01(self, mocker):
        game = Kazuoboe("sara", "martin")
        mocker.patch('random.uniform', return_value=0.3)
        game.decide_order()
        assert game.cur_player.name == "martin"

    def test_decide_order_02(self, mocker):
        game = Kazuoboe("sara", "martin")
        mocker.patch('random.uniform', return_value=0.8)
        game.decide_order()
        assert game.cur_player.name == "sara"

    def test_change_turn(self, mocker):
        game = Kazuoboe("sara", "martin")
        mocker.patch('random.uniform', return_value=0.3)
        game.decide_order()
        for _ in range(2): game.change_turn()
        assert game.cur_player.name == "martin"

        for _ in range(3): game.change_turn()
        assert game.cur_player.name == "sara"

    def test_new_num_is_in_range(self):
        game = Kazuoboe("sara", "martin")
        assert game.new_num_is_in_range(25, 20, 30)
        assert not game.new_num_is_in_range(35, 20, 30)

    # このメソッドのtestをするのに他のメソッドの影響を受けてる
    # 受けないように手動で正しい状況を作り出す？
    def test_add_new_num(self):
        game = Kazuoboe("sara", "martin")
        game.decide_order()
        cur_numbers = copy.deepcopy(game.cur_player.numbers)
        game.add_new_num(30)
        assert game.cur_player.numbers == cur_numbers + [30]
        assert game.cur_player.numbers != cur_numbers + [3]

    def test_ans_is_correct(self):
        game = Kazuoboe("sara", "martin")
        game.decide_order()
        game.cur_player.numbers = [34, 3, 56]
        assert game.ans_is_correct(1, 3)
        assert not game.ans_is_correct(2, 57)
