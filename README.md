# Raspberry-RCS620S
https://qiita.com/rukihena/items/3940ffa968c4c6492279

上記の記事を参照して作成した。
Rasberry Pi系で使用可能、Zero Wのみで検証済み
要 シリアル通信の設定、シリーズごとに異なる。

How To Use

1.lwiringPiのインストールが必要
$ sudo apt-get install libi2c-dev

2.本プロジェクトをクローン
$ git clone https://github.com/IrosSoftware/Raspberry-RCS620S.git

3.ディレクトリに移動してビルド
$ make getIDm

4.実行
$ ./getIDm

記事を基本参照だが、そのままでは動作しない点があったので、Makefileとソースコードを一部書き換えている。


追記　Python対応
https://qiita.com/rukihena/items/476d48e1e8d8fc6b98bf#_reference-e396793bfda9cc109c2c
上記の記事参照
