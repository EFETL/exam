#!/usr/bin/env python3
"""國小英文段考闖關產生器。

以國中英文闖關頁（jh/english/jh7-kangxuan/index.html）當引擎模板：
保留音效、交卷給老師、快問快答、配對、分類、選擇題、錯題本、手寫筆等共用程式，
把「資料區」「首頁考點雷達」「動畫」「綜合頁」換成國小版本。

用法：python3 scripts/es-english/build.py            （產生全部開放的冊別）
資料：scripts/es-english/books/<path>.py 裡的 BOOK 字典（題目全數自編，不含學校名稱）。
"""
import hashlib, html, importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
TPL = os.path.join(ROOT, 'jh/english/jh7-kangxuan/index.html')
TPL_T = [f for f in os.listdir(os.path.join(ROOT, 'jh/english/jh7-kangxuan')) if f.startswith('teacher-')][0]
TPL_T = os.path.join(ROOT, 'jh/english/jh7-kangxuan', TPL_T)
OUT = os.path.join(ROOT, 'es/english')

js = lambda o: json.dumps(o, ensure_ascii=False)


def cut(s, start, end, new, inclusive_end=False):
    i = s.index(start)
    j = s.index(end, i)
    if inclusive_end:
        j += len(end)
    return s[:i] + new + s[j:]


def load(path):
    spec = importlib.util.spec_from_file_location('b', path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.BOOK


# ---------- 國小專用：動畫（emoji 場景）、首頁、綜合頁 ----------
ES_CSS = r"""
/* ===== 可愛風格 ===== */
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;800&display=swap');
:root{--bg:#fff7fb;--line:#f6d9e6;--hi:#fff1c9;--ok:#38b07a;--bad:#f0647a;--shadow:0 6px 0 rgba(233,170,200,.35),0 10px 24px rgba(200,120,170,.12)}
body{background-color:var(--bg);background-image:radial-gradient(#ffd6e8 1.4px,transparent 1.6px),radial-gradient(#d9ecff 1.4px,transparent 1.6px);background-size:34px 34px;background-position:0 0,17px 17px}
.en,.qword,.ps,.etag{font-family:"Baloo 2",Nunito,"Noto Sans TC",sans-serif}
header.hero{position:relative;overflow:hidden;border-radius:0 0 36px 36px;padding:34px 0 40px}
header.hero::after{content:"⭐ 🌈 ☁️ 🍭 ⭐";position:absolute;right:18px;top:14px;font-size:1.6rem;letter-spacing:.3em;opacity:.85;animation:bob 3s ease-in-out infinite}
.hero h1{text-shadow:0 3px 0 rgba(0,0,0,.12)}
.mascot{position:absolute;right:22px;bottom:-6px;font-size:4.2rem;animation:bob 2.6s ease-in-out infinite;filter:drop-shadow(0 4px 4px rgba(0,0,0,.15))}
.mascot b{position:absolute;right:70px;top:-6px;font-size:.95rem;background:#fff;color:#c2477e;border-radius:16px 16px 4px 16px;padding:4px 12px;white-space:nowrap;box-shadow:0 3px 8px rgba(0,0,0,.12)}
@media(max-width:640px){.mascot{font-size:3rem}.mascot b{display:none}header.hero::after{display:none}}
.card{border-radius:26px!important;border:3px solid #fde3ee;box-shadow:var(--shadow)!important}
.tab{border-radius:99px!important;border:2px solid #fbd3e4!important;font-weight:700}
.tab.on{box-shadow:0 4px 0 rgba(0,0,0,.15)}
.sub{border-radius:18px!important;font-weight:700}
.btn,.opt,.o{border-radius:18px!important;transition:transform .12s}
.btn{box-shadow:0 4px 0 rgba(0,0,0,.18)}
.btn:active,.opt:active,.o:active{transform:translateY(3px) scale(.98)}
.opt{border-width:3px!important;font-size:1.15rem}
.opt.ok,.o.ok{animation:yay .5s ease}
@keyframes yay{0%{transform:scale(1)}40%{transform:scale(1.08) rotate(-2deg)}100%{transform:scale(1)}}
.lc{border-radius:24px!important;box-shadow:0 6px 0 rgba(0,0,0,.12)!important;position:relative;overflow:hidden}
.lc::after{content:"";position:absolute;right:-20px;bottom:-20px;width:90px;height:90px;border-radius:50%;background:rgba(255,255,255,.18)}
.chips span{border-radius:99px!important}
.fill{background:linear-gradient(90deg,#ff9ac1,#ffd166)!important;border-radius:99px}
.track{border-radius:99px!important}
.estage{border-radius:28px!important;background:linear-gradient(160deg,#fff4fb,#ffe6f1 50%,#e6f3ff)!important;border:3px dashed #ffc2db}
.estage img{max-height:78%;max-width:92%;border-radius:22px;box-shadow:0 6px 18px rgba(0,0,0,.12);animation:popin .5s ease both}
.lc .cv{position:absolute;right:10px;bottom:8px;width:64px;height:64px;border-radius:16px;object-fit:cover;opacity:.95}
.tagbadge{display:inline-block;font-size:.8rem;border-radius:99px;padding:0 8px;margin-left:6px;background:#ffe3ef;color:#b0306a;vertical-align:middle}
/* 國小版：emoji 場景舞台 */
.estage{position:relative;aspect-ratio:16/9;border-radius:16px;overflow:hidden;background:linear-gradient(160deg,#fff7e0,#ffe2c2 55%,#ffd0a8);display:flex;align-items:center;justify-content:center;flex-direction:column}
.estage .emo{font-size:clamp(3.2rem,11vw,7rem);line-height:1.15;text-align:center;letter-spacing:.08em;animation:bob 2.4s ease-in-out infinite}
.estage .emo span{display:inline-block;animation:popin .6s ease both}
.estage .etag{margin-top:12px;background:rgba(255,255,255,.9);border-radius:99px;padding:6px 18px;font-weight:900;font-size:1.25rem;color:#5b3a12;font-family:Nunito,"Noto Sans TC",sans-serif;max-width:92%;text-align:center}
.estage .esay{position:absolute;right:12px;top:12px;border:none;background:#fff;border-radius:99px;padding:6px 14px;font-weight:700;box-shadow:0 2px 8px rgba(0,0,0,.12)}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
@keyframes popin{from{transform:scale(.3);opacity:0}to{transform:scale(1);opacity:1}}
.exam-h{margin:26px 0 10px;font-size:1.15rem;color:var(--main);font-weight:900}
.chips span.n0{opacity:.6}
.vtable{width:100%;border-collapse:collapse;font-size:1rem}
.vtable th,.vtable td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left}
.vtable th{color:var(--muted);font-weight:500}
"""

ES_JS = r"""
/* ================= 國小版：單元動畫（emoji 場景＋句型） ================= */
function eStage(){return `<div class="estage" id="es"><button class="esay" id="esSay">🔊 聽一聽</button><div class="emo" id="esE"></div><div class="etag en" id="esT"></div></div>`}
function showScene(st){
  const E=$('#esE'),T=$('#esT');if(!E)return;
  E.innerHTML=st.img&&IMGS.has(st.img)?`<img src="img/${st.img}.png" alt="">`:[...st.emo].filter(c=>c.trim()).map((c,i)=>`<span style="animation-delay:${i*.12}s">${c}</span>`).join('');
  T.textContent=st.tag||'';
  $('#esSay').onclick=()=>say(st.tag||'');
}
function animUnit(p){
  const d=L[cur];
  p.innerHTML=`<div class="card">${eStage()}<div class="steps"></div><div class="caption"></div></div>
  <div class="card"><h3>🗺️ ${esc(d.no)} 一張圖</h3>${(d.map||[]).map(([a,b])=>`<p><span class="pill">${a}</span>${b}</p>`).join('')}</div>
  ${d.vocab?`<div class="card"><h3>📒 本課單字（點一下聽發音）</h3><div class="chips">${d.vocab.map(([w,c])=>`<span class="en vw" data-w="${esc(w)}">${esc(w)} <b>${esc(c)}</b></span>`).join('')}</div></div>`:''}`;
  p.querySelectorAll('.vw').forEach(s=>{s.style.cursor='pointer';s.onclick=()=>say(s.dataset.w)});
  stepper(p,d.scenes,i=>{showScene(d.scenes[i]);say(d.scenes[i].tag||'')},7000);
}
function animMorph(p){
  const d=L[cur],S=d.morph;
  p.innerHTML=`<div class="card"><h3>🎬 句型變身秀：同一句話，變成否定、問句、回答！</h3>
    <p class="muted">先選一句，再按下面的按鈕看它怎麼變身（會唸出來）。</p>
    <div class="row" id="pk">${S.map((s,i)=>`<button class="sub" data-i="${i}">${s.tag}</button>`).join('')}</div>
    <div class="ps en" id="ps" style="margin-top:14px"></div>
    <div class="row" id="pv" style="margin-top:12px;justify-content:center"></div>
    <div class="meaning" id="pm">👆 請按上面的按鈕</div></div>
    <div class="card"><h3>🎯 必考速記</h3>${(d.tips||[]).map(([a,b])=>`<p><span class="pill">${a}</span>${b}</p>`).join('')}</div>`;
  function show(i){
    const s=S[i];p.querySelectorAll('#pk .sub').forEach(b=>b.classList.toggle('on',+b.dataset.i===i));
    $('#ps').innerHTML=esc(s.raw);$('#pm').innerHTML='👆 請按變身按鈕';
    $('#pv').innerHTML=s.v.map((v,k)=>`<button class="btn ${k%2?'alt':''}" data-k="${k}">${v.n}</button>`).join('');
    $('#pv').querySelectorAll('button').forEach(b=>b.onclick=()=>{
      const v=s.v[+b.dataset.k];
      const ps=$('#ps');ps.innerHTML=v.t;ps.classList.remove('pop');void ps.offsetWidth;ps.classList.add('pop');
      $('#pm').innerHTML='💡 '+v.m;say(ps.textContent);
    });
  }
  p.querySelectorAll('#pk .sub').forEach(b=>b.onclick=()=>show(+b.dataset.i));
  show(0);
}
const ANIM=new Proxy({},{get:(o,k)=>L[k]&&L[k].morph?animMorph:animUnit});

/* ================= 首頁：考點雷達（國小版） ================= */
function renderHome(app){
  const R=RADAR;
  const bar=(arr,M)=>`<div class="bars">${arr.map(([n,v])=>`<div class="b"><span>${n}</span><div class="track"><div class="fill" data-w="${M?v/M*100:0}"></div></div><b>${v}/${M}</b></div>`).join('')}</div>`;
  const cards=ks=>ks.map(k=>`<div class="lc" style="background:${L[k].color}" data-k="${k}"><div><div class="n">${L[k].no}</div><div class="t">${L[k].short}</div></div><div class="d">${L[k].desc}</div></div>`).join('');
  app.innerHTML=`
  <h2>📡 段考考點雷達</h2>
  <p class="muted">${R.intro}</p>
  ${EXAMS.map(e=>`<div class="exam-h">${e.name}｜${e.range}</div><div class="lessoncards" style="margin:8px 0 8px">${cards(e.units)}</div>`).join('')}
  <div class="exam-h">共同練習</div>
  <div class="lessoncards" style="margin:8px 0 24px">${cards(COMMON)}
    <div class="lc" style="background:linear-gradient(135deg,#5a3a24,#9a7350)" data-k="mix"><div><div class="n">綜合</div><div class="t">閱讀＋克漏字</div></div><div class="d">原創短文｜看圖對話｜中翻英翻翻卡</div></div>
  </div>
  ${R.papers.map(pp=>`<div class="card"><h3>${pp.title}</h3>
    ${pp.n?`<p class="muted">${pp.note}</p>${bar(pp.topics,pp.n)}`:`<p class="muted">${pp.note}</p>`}
    ${pp.types&&pp.types.length?`<h3 style="margin-top:16px">📝 題型（幾份考卷有考）</h3><div class="chips">${pp.types.map(([w,n])=>`<span>${w} <b>×${n}</b></span>`).join('')}</div>`:''}
    ${pp.words&&pp.words.length?`<h3 style="margin-top:16px">🔤 常考單字句型</h3><div class="chips">${pp.words.map(w=>`<span class="en">${esc(w)}</span>`).join('')}</div>`:''}
    ${pp.tip?`<p class="muted" style="margin-top:12px">⚠️ ${pp.tip}</p>`:''}</div>`).join('')}
  <div class="card"><h3>🧭 建議闖關順序</h3>
  <p>① 每課先看 <b>🎬 動畫導覽</b>，跟著唸單字和句子 → ② <b>⚡ 單字快問快答</b>、<b>🔗 句子配對</b> → ③ <b>🔤 字母與發音</b>、<b>🧱 句型特訓</b> → ④ <b>📝 段考模擬題</b>與 <b>🧩 閱讀＋克漏字</b>，做完按「交卷給老師」。</p>
  <p class="muted">各校段考範圍略有不同，請以學校公告為準。本站題目全數自編，沒有使用任何學校的考卷原題。</p></div>`;
  app.querySelectorAll('.lc').forEach(c=>c.onclick=()=>go(c.dataset.k,c.dataset.k==='mix'?undefined:'anim'));
  requestAnimationFrame(()=>setTimeout(()=>app.querySelectorAll('.fill').forEach(f=>f.style.width=f.dataset.w+'%'),60));
}

/* ================= 綜合：閱讀＋克漏字＋翻譯（國小版） ================= */
function renderMix(app){
  const s=curSub.mix||'read';
  const subs=[['read','📖 閱讀測驗'],['cloze','🧩 克漏字'],['trans','🃏 中翻英翻翻卡']];
  app.innerHTML=`<h2>🧩 閱讀＋克漏字＋翻譯</h2>
  <p class="muted">${MIXNOTE}</p>
  <div class="subtabs">${subs.map(([k,t])=>`<button class="sub ${k===s?'on':''}" data-s="${k}">${t}</button>`).join('')}</div><div id="panel"></div>`;
  app.querySelectorAll('.sub').forEach(b=>b.onclick=()=>{curSub.mix=b.dataset.s;render()});
  const p=$('#panel');
  if(s==='trans'){
    p.innerHTML=`<div class="card"><h3>🃏 中翻英翻翻卡</h3><p class="muted">先在心裡（或紙上）說出英文，再點卡片翻面對答案，會唸給你聽。</p>
    <div class="flips tr">${TRANS.map((c,k)=>`<div class="flip" data-k="${k}"><div class="in"><div class="f"><b>${esc(c[0])}</b></div><div class="bk2"><span class="en">${esc(c[1])}</span><small>${esc(c[2])}</small></div></div></div>`).join('')}</div></div>`;
    p.querySelectorAll('.flip').forEach(f=>f.onclick=()=>{f.classList.toggle('on');if(f.classList.contains('on'))say(TRANS[+f.dataset.k][1])});
    return;
  }
  const set=s==='cloze'?CLOZE:READ;
  p.innerHTML=set.map((c,k)=>`<div class="card"><h3>${c.title} <button class="say" data-k="${k}">🔊</button></h3><div class="passage en">${esc(c.text).replace(/\n/g,'<br>').replace(/__(\d)__/g,'<b class="blank">__$1__</b>')}</div><div id="cq${k}"></div></div>`).join('');
  p.querySelectorAll('h3 .say').forEach(b=>b.onclick=()=>say(set[+b.dataset.k].text.replace(/__\d__/g,'blank')));
  set.forEach((c,k)=>{const nm=c.title.split('｜')[1]||c.title;renderMCQ($('#cq'+k),c.qs.map(q=>({...q,src:'',q:/^__\d__$/.test(q.q)?`${nm} 第 ${q.q.replace(/_/g,'')} 格`:q.q})),8,`綜合 ${c.title.replace(/｜/g,' ')}`)});
}

meChip();drawTabs();render();
if(!CLOUD.me)enroll(()=>{},true);
"""

ASK = {'e': '選出正確的中文意思', 'c': '選出正確的英文', 's': '選出正確的拼字', 'u': '選出正確的大小寫／字母',
       'g': '選出正確的句子', 'h': '選出正確的回答', 'z': '選出畫線部分發音相同的字', 'l': '選出缺少的字母',
       'p': '選出正確的複數'}


# ---------- 原卷題、挑戰題 ----------
def merge_extra(book):
    L = book['units']
    hp = os.path.join(HERE, 'hard', book['path'] + '.py')
    if os.path.exists(hp):
        spec = importlib.util.spec_from_file_location('h', hp); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        H = m.HARD
        for k, qs in H.get('units', {}).items():
            L[k]['hard'] = qs
        for k, qs in H.get('quick', {}).items():
            L[k]['quick'] = L[k]['quick'] + qs
        book['cloze'] = book['cloze'] + H.get('cloze', [])
        book['read'] = book['read'] + H.get('read', [])
    key = book['path'].replace('-exam2', '')
    orig = json.load(open(os.path.join(HERE, 'orig.json'), encoding='utf-8'))
    for q in orig:
        if q['book'] != key:
            continue
        u = q['unit'] if q['unit'] in L and q['unit'] != 'review' else 'gram'
        L[u].setdefault('orig', []).append({'q': q['q'].replace('\n', '　'), 'o': q['o'], 'a': q['a'], 'src': '原卷題', 'ex': q['ex']})
    for d in L.values():
        if 'subs' in d:
            d['subs'] = d['subs'] + ([['orig', '📄 原卷題']] if d.get('orig') else []) + ([['hard', '🔥 挑戰題']] if d.get('hard') else [])


# ---------- 微軟 Neural 語音（edge-tts 預錄 mp3；檔名＝頁面 akey() 的 FNV-1a 雜湊） ----------
VOICE = 'en-US-AnaNeural'
IS_EN = re.compile(r"^[A-Za-z][A-Za-z0-9 '’\-/.…,?!\"]*$")


def norm_say(t):
    t = re.sub(r'<br\s*/?>', ' ', t, flags=re.I); t = re.sub(r'<[^>]+>', '', t); t = html.unescape(t)
    t = t.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"').replace('…', ' ')
    t = re.sub(r'___+', 'blank', t)
    return re.sub(r'\s+', ' ', t).strip()


def akey(t):
    h = 0x811c9dc5
    b = t.encode('utf-16-le')
    for i in range(0, len(b), 2):
        h ^= b[i] | (b[i + 1] << 8)
        h = (h * 0x01000193) & 0xffffffff
    return '%08x' % h


def say_texts(book):
    out = set()
    add = lambda t: out.add(norm_say(t)) if t and norm_say(t) else None
    for d in book['units'].values():
        for it in d.get('quick', []):
            q, a, typ = it[0], it[1], it[4]
            if IS_EN.match(q.strip()) and typ not in 'su': add(q)
            if IS_EN.match(a.strip()) and typ not in 'eu': add(a)
        for sc in d.get('scenes', []): add(sc.get('tag', ''))
        for w in d.get('vocab', []): add(w[0])
        for mo in d.get('morph', []):
            for v in mo['v']: add(v['t'])
    for t in book['trans']: add(t[1])
    for c in book['cloze'] + book['read']: add(re.sub(r'__\d__', 'blank', c['text']))
    return out


def make_audio(book, adir):
    import asyncio
    texts = {akey(t): t for t in say_texts(book)}
    os.makedirs(adir, exist_ok=True)
    have = {f[:-4] for f in os.listdir(adir) if f.endswith('.mp3')}
    for k in have - set(texts):
        os.remove(os.path.join(adir, k + '.mp3'))
    todo = [(k, t) for k, t in texts.items() if k not in have]
    if todo:
        import edge_tts
        proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
        sem = asyncio.Semaphore(6)

        async def one(k, t):
            spoken = re.sub(r'[^\x20-\x7e]', ' ', t).replace('/', ' or ')
            async with sem:
                for _ in range(4):
                    try:
                        await edge_tts.Communicate(spoken, VOICE, rate='-8%', proxy=proxy).save(os.path.join(adir, k + '.mp3'))
                        return
                    except Exception as e:
                        err = e; await asyncio.sleep(2)
                print('  語音失敗', t[:40], err)

        async def run():
            await asyncio.gather(*(one(k, t) for k, t in todo))
        asyncio.run(run())
        print(f'  新增語音 {len(todo)} 個')
    return {f[:-4] for f in os.listdir(adir) if f.endswith('.mp3') and os.path.getsize(os.path.join(adir, f)) > 0}


def build(book):
    tpl = open(TPL, encoding='utf-8').read()
    subj = book['subject']
    path = book['path']
    s = tpl
    # 標題與頁首
    s = re.sub(r'<title>.*?</title>', f"<title>{book['title']}｜{book['ver']}</title>", s, count=1)
    s = s.replace('</style>', ES_CSS + '\n</style>', 1)
    hero = f'''<header class="hero">
  <div class="wrap">
    <a href="../" style="color:#fff;opacity:.85;text-decoration:none;font-size:1rem;display:block;margin-bottom:8px">← 回英文選單</a><span class="tag">{book['tag']}</span>
    <h1>{book['h1']}</h1>
    <p>{book['lead']}</p>
    <div class="me" id="me"></div>
  </div>
  <div class="mascot">{book.get('mascot','🐰')}<b>{book.get('cheer','一起闖關，加油！')}</b></div>
</header>'''
    s = cut(s, '<header class="hero">', '</header>', hero, inclusive_end=True)
    s = cut(s, '<footer>', '</footer>', '<footer><div class="wrap">全民補習班 ‧ 國小英文段考闖關 ‧ 自編題＋原卷題　發音：微軟 Neural 英語語音</div></footer>', inclusive_end=True)
    s = s.replace(':root{\n  --main:#8a3b12; --main-2:#c4682f;', ':root{\n  --main:%s; --main-2:%s;' % tuple(book['theme']), 1)
    s = s.replace('linear-gradient(135deg,#5e2709 0%,#b5652b 60%,#f2c14e 140%)', book['hero_bg'], 1)

    # 資料區
    L = book['units']
    merge_extra(book)
    imgs = sorted(f[:-4] for f in os.listdir(os.path.join(OUT, path, 'img')) if f.endswith('.png')) if os.path.isdir(os.path.join(OUT, path, 'img')) else []
    for k, d in L.items():
        for i, sc in enumerate(d.get('scenes', [])):
            sc['img'] = f'{k}-{i}'
    audio = make_audio(book, os.path.join(OUT, path, 'audio'))
    data = ['/* ================= 資料（國小版，題目全數自編） ================= */',
            'const ASK=' + js(ASK) + ';',
            'const L=' + js(L) + ';',
            'const EXAMS=' + js(book['exams']) + ';',
            'const COMMON=' + js(book['common']) + ';',
            'const CLOZE=' + js(book['cloze']) + ';',
            'const READ=' + js(book['read']) + ';',
            'const TRANS=' + js(book['trans']) + ';',
            'const RADAR=' + js(book['radar']) + ';',
            'const MIXNOTE=' + js(book['mixnote']) + ';',
            'const TABS=' + js(book['tabs']) + ';',
            'const IMGS=new Set(' + js(imgs) + ');',
            'const AUDIO=new Set(' + js(sorted(audio)) + ');', '']
    s = cut(s, '/* ================= 資料 ================= */', '/* ================= 注釋配對', '\n'.join(data) + '\n')
    # 交卷設定
    s = s.replace('eng7-kangxuan-1', subj)
    s = s.replace("site:'英文 國一上第一次段考（康軒）'", f"site:'{book['site']}'")
    assert 'eng7-kangxuan' not in s, 'subject 沒換乾淨'
    # 動畫、首頁、綜合
    s = cut(s, 'const ANIM={', 'function isAnim', '')
    s = cut(s, '/* ================= 首頁：考點雷達 ================= */', '/* ================= 快問快答（英文版＋交卷） ================= */', '')
    s = cut(s, '/* ================= 綜合：克漏字＋閱讀＋翻譯 ================= */', '/* ================= ✏️ 老師手寫', ES_JS + '\n')
    # 國小：配對的標題改「句子配對」
    s = s.replace("['match','🔗 片語配對']", "['match','🔗 句子配對']")
    s = s.replace("['mcq','📝 段考模擬題']];", "['mcq','📝 段考模擬題'],...(d.orig&&d.orig.length?[['orig','📄 原卷題']]:[]),...(d.hard&&d.hard.length?[['hard','🔥 挑戰題']]:[])];", 1)
    s = s.replace("  if(s==='mcq') renderMCQ(p,d.mcq,d.code,title);", "  if(s==='mcq') renderMCQ(p,d.mcq,d.code,title);\n  if(s==='orig') renderMCQ(p,d.orig,d.code,title+' 原卷題');\n  if(s==='hard') renderMCQ(p,d.hard,d.code,title+' 挑戰題');", 1)
    s = s.replace("const isEN=s=>/^[A-Za-z][A-Za-z '’\\-\\/.…]*$/.test(s.trim());", "const isEN=s=>/^[A-Za-z][A-Za-z0-9 '’\\-\\/.…,?!\"]*$/.test(s.trim());", 1)
    s = s.replace("for(const arr of [d.mcq,d.gmcq]){", "for(const arr of [d.mcq,d.gmcq,d.orig,d.hard]){", 1)
    for chk in ["['orig','📄 原卷題']", "if(s==='hard')", "0-9 '", "d.orig,d.hard]"]:
        assert chk in s, chk
    for bad in ['康軒課本', '19 校', 'Get Ready']:
        pass
    os.makedirs(os.path.join(OUT, path), exist_ok=True)
    open(os.path.join(OUT, path, 'index.html'), 'w', encoding='utf-8').write(s)

    # 老師端
    t = open(TPL_T, encoding='utf-8').read()
    t = t.replace("const SUBJECT='eng7-kangxuan-1';", f"const SUBJECT='{subj}';")
    unit = {str(d['code']): f"{d['no']} {d['title']}" for d in L.values()}
    unit['8'] = '閱讀＋克漏字'
    t = re.sub(r'const UNIT=\{.*?\};', 'const UNIT=' + js(unit) + ';', t, count=1)
    t = re.sub(r'<h1>.*?</h1><p>.*?</p>', f"<h1>📊 {book['site']}｜老師端</h1><p>{book['range_all']}：學生交卷的姓名、分數與錯題（開啟即自動讀取）</p>", t, count=1)
    t = t.replace('段考闖關成績_國一英文康軒.csv', f"段考闖關成績_{subj}.csv")
    assert 'eng7-kangxuan' not in t
    tname = 'teacher-' + hashlib.sha1(('efetl-es-' + subj).encode()).hexdigest()[:8] + '.html'
    for f in os.listdir(os.path.join(OUT, path)):
        if f.startswith('teacher-') and f != tname:
            os.remove(os.path.join(OUT, path, f))
    open(os.path.join(OUT, path, tname), 'w', encoding='utf-8').write(t)
    return tname


if __name__ == '__main__':
    bdir = os.path.join(HERE, 'books')
    names = sys.argv[1:] or sorted(f[:-3] for f in os.listdir(bdir) if f.endswith('.py') and not f.startswith('_'))
    for n in names:
        b = load(os.path.join(bdir, n + '.py'))
        print(n, '→', build(b))
