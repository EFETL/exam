#!/usr/bin/env python3
"""國小英文段考闖關產生器。

以國中英文闖關頁（jh/english/jh7-kangxuan/index.html）當引擎模板：
保留音效、交卷給老師、快問快答、配對、分類、選擇題、錯題本、手寫筆等共用程式，
把「資料區」「首頁考點雷達」「動畫」「綜合頁」換成國小版本。

用法：python3 scripts/es-english/build.py            （產生全部開放的冊別）
資料：scripts/es-english/books/<path>.py 裡的 BOOK 字典（題目全數自編，不含學校名稱）。
"""
import hashlib, importlib.util, json, os, re, sys

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
  E.innerHTML=[...st.emo].filter(c=>c.trim()).map((c,i)=>`<span style="animation-delay:${i*.12}s">${c}</span>`).join('');
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
</header>'''
    s = cut(s, '<header class="hero">', '</header>', hero, inclusive_end=True)
    s = cut(s, '<footer>', '</footer>', '<footer><div class="wrap">全民補習班 ‧ 國小英文段考闖關 ‧ 題目全數自編　發音：瀏覽器英語語音</div></footer>', inclusive_end=True)
    s = s.replace(':root{\n  --main:#8a3b12; --main-2:#c4682f;', ':root{\n  --main:%s; --main-2:%s;' % tuple(book['theme']), 1)
    s = s.replace('linear-gradient(135deg,#5e2709 0%,#b5652b 60%,#f2c14e 140%)', book['hero_bg'], 1)

    # 資料區
    L = book['units']
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
            'const AUDIO=new Set([]);', '']
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
