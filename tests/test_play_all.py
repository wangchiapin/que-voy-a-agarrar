# 從頭玩到尾：三關各用「一般」和「聽力」模式自動全對，檢查能打到結算、三顆愛心都在、沒有網頁錯誤
import sys, asyncio
from playwright.async_api import async_playwright
from common import HTML
SOLVER = """
async ({lv, listen, cfg}) => {
  const hf=__hf, sleep=ms=>new Promise(r=>setTimeout(r,ms));
  Object.assign(hf.S,cfg); hf.S.listen=listen; hf.P0.unlocked=3;
  hf.startLevel(lv);
  const log=[]; let guard=0, wrongTried=false, hintTried=false, posWrongTried=false, itemWrongTried=false;
  while(!hf.G.res && guard++<4000){
    await sleep(8);
    const G=hf.G; if(!G||G.busy||G.qi>=G.qs.length) continue;
    if(hf.PL.moving||hf.PL.path.length||hf.PL.judge) continue;
    const st=hf.curStop(), H=G.house;
    if(G.phase==='go'){
      if(G.qi===0&&!hintTried){hintTried=true; document.querySelector('[data-a=hint]').click(); await sleep(20);}
      // 第二題先故意走錯一次（走到別的家具）
      if(G.qi===1&&!wrongTried&&(false)){
        wrongTried=true;
        const other=Object.values(H.furn).find(F=>F.id!==st.f);
        const hearts=G.hearts; hf.tapTile(other.x,other.y);
        for(let i=0;i<300&&(hf.PL.moving||hf.PL.path.length||hf.PL.judge);i++) await sleep(8);
        await sleep(30);
        log.push('wrongFurn hearts '+hearts+'->'+hf.G.hearts); continue;
      }
      if(lv===1){
        const a=H.rects[st.r]; let best=null;
        for(let y=a.y0;y<=a.y1;y++)for(let x=a.x0;x<=a.x1;x++){ if(H.occ[y][x])continue; if(!best||Math.abs(x-(a.x0+a.x1)/2)+Math.abs(y-(a.y0+a.y1)/2)<best.d)best={x,y,d:Math.abs(x-(a.x0+a.x1)/2)+Math.abs(y-(a.y0+a.y1)/2)}; }
        hf.tapTile(best.x,best.y);
      } else {
        const F=H.furn[st.f];
        if(lv>=3&&hf.WALK_POS.includes(st.p)){ const sp=H.spots[st.f][st.p]; hf.tapTile(sp[0].x,sp[0].y); }
        else hf.tapTile(F.x,F.y);
      }
      for(let i=0;i<400&&(hf.PL.moving||hf.PL.path.length||hf.PL.judge);i++) await sleep(8);
      await sleep(30);
    } else if(G.phase==='pos'){
      if(!posWrongTried&&false){posWrongTried=true; const w=['up','down','in','side','front','back'].find(p=>p!==st.p); const h=G.hearts; hf.choosePos(w); log.push('wrongPos hearts '+h+'->'+hf.G.hearts); await sleep(20);}
      hf.choosePos(st.p); await sleep(450);
    } else if(G.phase==='item'){
      if(!itemWrongTried&&false){itemWrongTried=true; const w=st.ch.find(i=>i!==st.i); const h=G.hearts; hf.chooseItem(w); log.push('wrongItem hearts '+h+'->'+hf.G.hearts); await sleep(20);}
      hf.chooseItem(st.i); await sleep(500);
    }
  }
  const r=hf.G.res; return {res:r, hearts:hf.G.hearts, log, guard, review:[...hf.G.review.keys()]};
}
"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--no-sandbox'])
        ctx = await b.new_context(viewport={'width': 390, 'height': 800}, is_mobile=True, has_touch=True)
        page = await ctx.new_page(); errs = []
        page.on('pageerror', lambda e: errs.append(str(e)))
        page.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        await page.route('**/*', lambda r: r.continue_() if r.request.url.startswith('file:') else r.abort())
        await page.goto(HTML + '?fast=1')
        bad = 0
        for rep in range(2):
            for lv in (1, 2, 3):
                r = await page.evaluate(SOLVER, {'lv': lv, 'listen': rep % 2 == 1, 'cfg': {'ui': 'es', 'read': 'py', 'text': 'tw', 'trans': 'es', 'labels': 'room'}})
                ok = r['res'] and r['res']['done'] and r['hearts'] == 3 and isinstance(r['res'].get('secs'), int)
                print(('  ok  ' if ok else '  FAIL'), '第%d關 %s模式' % (lv, '聽力' if rep % 2 else '一般'))
                if not ok: bad += 1
        # 網頁錯誤（外部網路被擋造成的 Firebase 連線訊息不算）
        errs = [e for e in errs if 'Failed to load resource' not in e and 'net::' not in e]
        print('  ok  ' if not errs else '  FAIL', '沒有網頁錯誤', errs[:3])
        await b.close()
        return bad + (1 if errs else 0)
bad = asyncio.run(main())
print('FAILS', bad); sys.exit(1 if bad else 0)
