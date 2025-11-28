#!/bin/bash -xv
# SPDX-FileCopyrightText: 2025 Keito Tadano
# SPDX-License-Identifier: GPL-3.0-only

ng () {
        echo "${1}行目が違うよ"
        res=1
}

res=0

CMD="./score.py"

### 引数なし ###
out=$($CMD 2>&1)
ret=$?
[ "$ret" != 0 ] || ng "$LINENO"
echo "$out" | grep -q "使い方" || ng "$LINENO"

### 無効なチーム名 ###
out=$($CMD "abcdefg" 2>&1)
ret=$?
[ "$ret" = 0 ] || ng "$LINENO"
echo "$out" | grep -q "入力したチーム名が見つかりません" || ng "$LINENO"

# 代表として Real Madrid が一覧に含まれているかチェック
echo "$out" | grep -q "Real Madrid" || ng "$LINENO"

### 有効なチーム名（例：Real Madrid）###
# スコアは毎日変わるので、パターンだけ確認
out=$($CMD "Real Madrid" 2>/dev/null)
ret=$?
[ "$ret" = 0 ] || ng "$LINENO"

# 「データがありません」または 「YYYY」「-」 を含むことを許容
echo "$out" | grep -Eq "データがありません|[0-9]{4}.*-.*" || ng "$LINENO"

### 異常文字列テスト ###
out=$($CMD "" 2>&1)
echo "$out" | grep -q "見つかりません" || ng "$LINENO"

out=$($CMD "@#$%^&*" 2>&1)
echo "$out" | grep -q "見つかりません" || ng "$LINENO"

out=$($CMD " " 2>&1)
echo "$out" | grep -q "見つかりません" || ng "$LINENO"

# 非ASCII・制御文字
out=$(echo -e "\x00\x01\x02" | xargs $CMD 2>&1)
echo "$out" | grep -q "見つかりません" || ng "$LINENO"

# 長すぎる入力
long_str=$(printf 'a%.0s' {1..500})
out=$($CMD "$long_str" 2>&1)
echo "$out" | grep -q "見つかりません" || ng "$LINENO"

[ "$res" = 0 ] && echo "OK"
exit "$res"


