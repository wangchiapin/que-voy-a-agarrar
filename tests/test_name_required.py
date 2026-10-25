# 結算畫面：沒填名字不給存入排行榜；填了才存
import sys
from playwright.sync_api import sync_playwright
from common import *
R = Runner()
with sync_playwright() as p:
    b, pg, errs = open_page(p, '?unlock=1&seed=5&fast=1')
    pg.evaluate("__hf.S.lang='es'"); pg.evaluate("__hf.startLevel(1)")
    pg.evaluate("endGame(true)"); pg.wait_for_timeout(600)
    R.check(pg.evaluate("!!document.getElementById('nm')"), '結算畫面有名字欄')
    pg.fill('#nm', '   '); pg.click('[data-a=saveScore]'); pg.wait_for_timeout(300)
    R.check(pg.evaluate("__hf.G.saved") in (False, None, 0), '空白名字：沒有存')
    R.check('Escribe tu nombre primero' in pg.evaluate("document.getElementById('toast').textContent"), '空白名字：跳出提示')
    R.check(not [o for o in pg.evaluate("window.__ops||[]") if o['k']=='set' and 'homefetchmap' in o['p']], '空白名字：沒有寫進排行榜')
    pg.fill('#nm', '小明'); pg.click('[data-a=saveScore]'); pg.wait_for_timeout(500)
    R.check(pg.evaluate("__hf.G.saved") is True, '填了名字：存入')
    sets = [o for o in pg.evaluate("window.__ops||[]") if o['k']=='set' and o['p'].startswith('homefetchmap_L1/')]
    R.check(len(sets)==1 and sets[0]['d']['name']=='小明' and isinstance(sets[0]['d'].get('secs'), int), '填了名字：寫進排行榜（含時間）')
    R.check(not errs, '沒有網頁錯誤 %s' % errs)
    b.close()
print('FAILS', R.fails); sys.exit(1 if R.fails else 0)
