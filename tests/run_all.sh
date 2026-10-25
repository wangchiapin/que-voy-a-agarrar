#!/bin/sh
# 在 tests 資料夾執行：sh run_all.sh   （需要 python3 + playwright + chromium）
cd "$(dirname "$0")" || exit 1
fail=0
for t in test_play_all.py test_name_required.py test_tiebreak.py; do
  echo "== $t"; python3 $t || fail=1
done
[ $fail = 0 ] && echo "全部通過" || echo "有項目沒過"
exit $fail
