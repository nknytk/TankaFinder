Tanka Finder
=====

入力された文章から短歌を見つけるWebサイト。  
[偶然短歌bot](https://twitter.com/g57577?lang=ja)に触発されて制作したもの。

使い方
-----

1. Ubuntu 16.04のサーバを用意する  
2. ソースコードをダウンロードする
3. `./setup.sh`を実行する。mecabやmecab-python3などの依存ライブラリがインストールされる
4. `./run.sh`を実行する
5. `http://<サーバ名>/static/index.html`にアクセスする

Ubuntu 14.04で使用する場合、`setup.sh`内の`# For Ubuntu 16.04`の下の行をコメントアウトし、  
`# For Ubuntu 14.04`の下の行頭の`#`を削除して有効化してください。

デモ
-----

http://210.129.50.127/static/index.html
