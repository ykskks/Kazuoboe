## TODO
- 範囲外の値が入力された時にフリーズしてしまう
- 全般的に例外対応が微妙、想定外の入力（入力なし）とかでも動いてしまう
- 今は範囲が広くて毎回区切りのいい数字で楽できてしまう。
    - 入力する必要性は必ずしもない
    - こちらから一方的に提案する？
    - 範囲を狭くする？

- validation?
    - 名前が空白でもスタートできてしまう...など
    - isinstance(input, int)とかでできるのかな

- bindを変えるところにデコレータ使ってもいいかな
    - rootとbutton毎回二つに設定しなあかんし、デコレータにした方が目立つ。
    - ゲームの移り変わりがわかりやすい

- rand, idxなどの変数名