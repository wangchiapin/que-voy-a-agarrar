# 共用：開頁面、擋外部網路、假 Firebase（會記住寫進去的資料，可模擬排行榜）
import os
from playwright.sync_api import sync_playwright
HTML = 'file://' + os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'index.html'))
APP = "export function initializeApp(c,n){return {c,n}}"
FS = '''
const DB=(window.__db=window.__db||{});
const op=(k,p,d)=>(window.__ops=window.__ops||[]).push({k,p,d});
export function getFirestore(app){return {app}}
export function initializeFirestore(app){return {app}}
export const collection=(db,...p)=>({db,path:p.join('/')});
export const doc=(db,...p)=>({db,path:p.join('/')});
export const serverTimestamp=()=>'SERVER_TS';
export async function setDoc(r,d){ if(window.__denySecs && 'secs' in d) throw new Error('permission-denied'); op('set',r.path,d); DB[r.path]=JSON.parse(JSON.stringify(d)); }
export async function addDoc(c,d){op('add',c.path,d);return {id:'P'+(window.__ops.length)}}
export async function updateDoc(r,d){op('update',r.path,d)}
export const getDoc=async(r)=>({exists:()=>r.path in DB,data:()=>DB[r.path]});
export const getDocs=async(q)=>{const c=q[0].path;const rows=Object.keys(DB).filter(k=>k.startsWith(c+'/')).map(k=>DB[k]).sort((a,b)=>b.score-a.score);const n=q[2]||999;const l=rows.slice(0,n);return {docs:l.map(d=>({data:()=>d})),size:l.length,forEach(){}}};
export const query=(...a)=>a,where=()=>0,orderBy=()=>0,limit=(n)=>n,onSnapshot=()=>()=>{},deleteDoc=async()=>{},increment=()=>0,runTransaction=async()=>{},writeBatch=()=>({}),Timestamp={now:()=>({}),fromDate:()=>({})},arrayUnion=()=>0,startAfter=()=>0,getCountFromServer=async()=>({data:()=>({count:0})}),documentId=()=>'id',enableIndexedDbPersistence=async()=>{};
'''
AUTH = """const a={currentUser:null,authStateReady:async()=>{}};
export const getAuth=()=>a,GoogleAuthProvider=class{};
export const signInAnonymously=async()=>{a.currentUser={uid:(window.__uid||'UID1'),isAnonymous:true};return {user:a.currentUser}};
export const onAuthStateChanged=(x,cb)=>{setTimeout(()=>cb(a.currentUser),0);return()=>{}};
export const signInWithPopup=async()=>{},signOut=async()=>{},signInWithCredential=async()=>{},setPersistence=async()=>{},browserLocalPersistence={};"""

def route(r):
    u = r.request.url
    if 'gstatic.com/firebasejs' in u:
        if 'compat' in u: return r.fulfill(status=200, content_type='application/javascript', body='')
        body = APP if 'firebase-app' in u else FS if 'firestore' in u else AUTH if 'auth' in u else ''
        return r.fulfill(status=200, content_type='application/javascript', body=body)
    if u.startswith('file:'): return r.continue_()
    r.abort()

class Runner:
    def __init__(self): self.fails = 0
    def check(self, cond, msg):
        print(('  ok  ' if cond else '  FAIL'), msg)
        if not cond: self.fails += 1

def open_page(p, query='', width=390, height=800, wait=1500):
    b = p.chromium.launch(args=['--no-sandbox'])
    pg = b.new_context(viewport={'width': width, 'height': height}).new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:150]))
    pg.route('**/*', route)
    pg.goto(HTML + query); pg.wait_for_timeout(wait)
    return b, pg, errs
