# 排行榜排序：分數高在前；同分時間短在前；舊紀錄（沒時間）同分排最後；每台裝置只留最好成績；規則沒更新時仍能存
import sys, json
from playwright.sync_api import sync_playwright
from common import *
R = Runner()
with sync_playwright() as p:
    b, pg, errs = open_page(p, '?unlock=1&fast=1')
    pg.evaluate("__hf.startLevel(1)")
    # 1) 排序函式
    rows = [{'name':'A','score':100,'secs':90},{'name':'B','score':100,'secs':40},{'name':'C','score':120,'secs':300},
            {'name':'D','score':100},{'name':'E','score':100,'secs':40}]
    order = pg.evaluate("rows=>Board.sort(rows).map(r=>r.name)", rows)
    R.check(order[0]=='C' and order[1:3]==['B','E'] and order[3]=='A' and order[4]=='D', '排序：分數高→時間短→舊紀錄最後 %s' % order)
    # 2) 線上榜：同一台裝置，同分時間更短會更新；時間更長不更新；分數更低不更新
    def put(score, secs, name='小明'):
        pg.evaluate("([s,t,n])=>Board.submit(1,n,s,false,t)", [score, secs, name]); pg.wait_for_timeout(200)
    doc = lambda: pg.evaluate("window.__db['homefetchmap_L1/UID1']")
    put(500, 100); d = doc(); R.check(d['score']==500 and d['secs']==100, '第一次存入')
    put(500, 150); d = doc(); R.check(d['score']==500 and d['secs']==100, '同分但更慢：不更新')
    put(500, 80);  d = doc(); R.check(d['score']==500 and d['secs']==80, '同分且更快：更新時間')
    put(400, 10);  d = doc(); R.check(d['score']==500 and d['secs']==80, '分數較低：不更新')
    put(600, 200); d = doc(); R.check(d['score']==600 and d['secs']==200, '分數更高：更新')
    # 3) 讀榜：多筆同分，時間短的排前面
    pg.evaluate("""()=>{window.__db['homefetchmap_L1/U2']={name:'乙',score:600,listen:false,secs:50};
                        window.__db['homefetchmap_L1/U3']={name:'丙',score:600,listen:false};
                        window.__db['homefetchmap_L1/U4']={name:'丁',score:700,listen:true,secs:999};}""")
    names = pg.evaluate("Board.top(1).then(r=>r.rows.map(x=>x.name))")
    R.check(names==['丁','乙','小明','丙'], '讀榜順序 %s' % names)
    # 4) 後台規則還沒更新（不接受 secs）：仍然存得進去
    pg.evaluate("window.__denySecs=true; window.__uid='X'")
    pg.evaluate("delete window.__db['homefetchmap_L2/UID1']")
    pg.evaluate("Board.submit(2,'阿華',300,false,70)"); pg.wait_for_timeout(300)
    d = pg.evaluate("window.__db['homefetchmap_L2/UID1']")
    R.check(d and d['score']==300 and 'secs' not in d, '舊規則：不帶時間也能存 %s' % d)
    # 5) 送出的欄位符合規則（只有 name/score/listen/updatedAt/secs；名字≤14；分數 0~20000；secs 0~86400）
    pg.evaluate("window.__denySecs=false")
    pg.evaluate("delete window.__db['homefetchmap_L3/UID1']")
    pg.evaluate("Board.submit(3,'小明小明小明小明小明小明小明小明',99999,true,999999)"); pg.wait_for_timeout(300)
    d = pg.evaluate("window.__db['homefetchmap_L3/UID1']")
    R.check(set(d)=={'name','score','listen','updatedAt','secs'} and len(d['name'])<=14 and d['score']==20000 and d['secs']==86400 and d['listen'] is True, '欄位與上限 %s' % json.dumps(d, ensure_ascii=False))
    R.check(not errs, '沒有網頁錯誤 %s' % errs)
    b.close()
print('FAILS', R.fails); sys.exit(1 if R.fails else 0)
