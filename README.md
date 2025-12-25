# robosys2025

本リポジトリは千葉工業大学 未来ロボティクス学科 2025年度 ロボットシステム学内で行った内容に基づいて作成された練習用リポジトリです。

# score
![CI](https://github.com/tadano0504/robosys2025/actions/workflows/test.yml/badge.svg)
## 概要
標準入力で与えられたLa Ligaに所属する全20チームに対して、
そのチームの **最新試合の日時・対戦相手・結果** を取得して表示するコマンドです。  
入力されたチーム名が存在しない場合は、利用可能なチーム一覧を表示します。

## テスト環境
OS            : Ubuntu 22.04.5 LTS / Windows 11  
python-version: 3.7 ~ 3.12  
確認環境      : Ubuntu 22.04.5 LTS + GitHub Actions (CI)

## 使用準備
下記のコマンドを使用し、クローンを行ってください。

```shell
$ git clone https://github.com/tadano0504/robosys2025.git
$ cd robosys2025
```

## 使い方
標準入力からチーム名を入力します。

実行例（Real Madrid の試合結果を取得）:

```shell
$ echo "Real Madrid" | ./score
 2025-11-26T20:00:00Z
 PAE Olympiakos SFP
 WIN 3-4
```

存在しないチーム名を入力した場合は、エラーと選択可能なチーム一覧が表示されます。

```shell
$ echo "abcdef" | ./score
 入力したチーム名が見つかりません
 Alaves
 Athletic Bilbao
 Atletico Madrid
 Barcelona
 Celta Vigo
 Elche
 Espanyol
 Getafe
 Girona
 Levante
 Mallorca
 Osasuna
 Rayo Vallecano
 Real Betis
 Real Madrid
 Real Oviedo
 Real Sociedad
 Sevilla
 Valencia
 Villarreal
```

入力が空またはスペースのみの場合も同様です。

## 入力仕様
- 標準入力で **チーム名を1 行入力** して渡す  
- 入力は英語表記のラ・リーガ所属チーム名に対応  
- 大文字・小文字は区別しない  
- 前後の空白は無視される  

不正な入力は以下のように扱われます。

- 空入力　　　　　　: `入力したチーム名が見つかりません` を表示し、チーム一覧を出力  
- 存在しない名前　　: `入力したチーム名が見つかりません` を表示し、チーム一覧を出力  
- 記号・制御文字など : `入力したチーム名が見つかりません` を表示し、チーム一覧を出力  
- 試合データなし　　 : `データがありません` を表示

## 著作権・ライセンス
- このソフトウェアパッケージは、GNU General Public License v3.0（GPL-3.0-only）の下、再頒布および使用が許可されています。
- この[README](https://github.com/tadano0504/robosys2025/blob/main/README.md)は、[asnm1208](https://github.com/asnm1208)の[robosys2025](https://github.com/asnm1208/robosys2024/blob/main/README.md)(© 2025 asnm1208)を参考に作られています。
- © 2025 Tadano Keito
