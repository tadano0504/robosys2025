#!/bin/bash -xv
# SPDX-FileCopyrightText: 2025 Keito Tadano
# SPDX-License-Identifier: GPL-3.0-only

ng () {
        echo "${1}行目が違うよ"
        res=1
}

res=0

CMD="./score.py"

out=$($CMD 2>&1)
ret=$?
[ "$ret" != 0 ] || ng "$LINENO"
echo "$out" | grep -q "使い方" || ng "$LINENO"

out=$($CMD "abcdefg" 2>&1)
ret=$?
echo "$out" | grep -q "入力したチーム名が見つかりません" || ng "$LINENO"
echo "$out" | grep -q "Real Madrid" || ng "$LINENO"

out=$( $CMD "Real Madrid" 2>/dev/null )
ret=$?
[ "$ret" = 0 ] || ng "$LINENO"
echo "$out" | grep -q "-" || ng "$LINENO"

[ "$res" = 0 ] && echo "OK"
exit $res

