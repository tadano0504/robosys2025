#!/bin/bash -xv
# SPDX-FileCopyrightText: 2025 Keito Tadano
# SPDX-License-Identifier: GPL-3.0-only

ng () {
    echo "${1}行目が違うよ"
    res=1
}

res=0
CMD="./score"

out=$(echo "" | $CMD 2>&1)
ret=$?
[ "$ret" = 1 ] || ng "$LINENO"
echo "$out" | grep -q "使い方" || ng "$LINENO"

out=$(echo "abcdefg" | $CMD 2>&1)
ret=$?
[ "$ret" = 0 ] || ng "$LINENO"
echo "$out" | grep -q "入力したチーム名が見つかりません" || ng "$LINENO"

out=$(echo "Real Madrid" | $CMD 2>&1)
ret=$?
[ "$ret" = 0 ] || ng "$LINENO"
echo "$out" | grep -Eq "データがありません|[0-9]{4}-[0-9]{2}-[0-9]{2}" || ng "$LINENO"

out=$(echo "@#$%^&*" | $CMD 2>&1)
echo "$out" | grep -q "見つかりません" || ng "$LINENO"

out=$(echo " " | $CMD 2>&1)
echo "$out" | grep -q "見つかりません" || ng "$LINENO"

out=$(echo -e "\x00\x01\x02" | $CMD 2>&1)
echo "$out" | grep -q "見つかりません" || ng "$LINENO"

long_str=$(printf 'a%.0s' {1..500})
out=$(echo "$long_str" | $CMD 2>&1)
echo "$out" | grep -q "見つかりません" || ng "$LINENO"

[ "$res" = 0 ] && echo "OK"
exit "$res"

