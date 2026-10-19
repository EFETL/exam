/* 段考闖關總入口：依 catalog.json 畫「學段 → 科目 → 冊別」卡片。
   每個資料夾的 index.html 只放 <main id="hub"></main> 並載入這支；它依網址判斷現在在哪一層。
   catalog.json 的 status：open＝開放、soon＝敬請期待（灰色不能點）、closed＝暫停開放（不顯示）。 */
(function(){
  const me=document.currentScript.src, ROOT=me.slice(0,me.lastIndexOf('/assets/')+1);
  const rel=location.href.split('#')[0].split('?')[0].slice(ROOT.length).replace(/index\.html$/,'');
  const seg=rel.split('/').filter(Boolean);
  const hub=document.getElementById('hub'), crumb=document.getElementById('crumb'), h1=document.getElementById('h1'), sub=document.getElementById('sub');
  const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const VC={翰林:['#2f6fb3','#4a97da'],康軒:['#e29a2e','#f2b350'],南一:['#2e9e6b','#48c08a'],龍騰:['#7a2f5c','#b04a86']};
  const card=(href,title,desc,emoji,c1,c2,badge,soon)=>`<${soon?'div':'a href="'+href+'"'} class="cardx${soon?' soon':''}" style="--c1:${c1};--c2:${c2}">
      <div class="top"><span class="emo">${emoji}</span>${badge?`<span class="badge">${esc(badge)}</span>`:''}</div>
      <div class="body"><h2>${esc(title)}</h2>${desc?`<p>${esc(desc)}</p>`:''}<span class="go">${soon?'敬請期待':'進入 →'}</span></div></${soon?'div':'a'}>`;
  const shade=(hex,k)=>{const n=parseInt(hex.slice(1),16),f=x=>Math.min(255,Math.round(x+(255-x)*k));return '#'+[f(n>>16),f(n>>8&255),f(n&255)].map(v=>v.toString(16).padStart(2,'0')).join('')};
  function crumbs(parts){crumb.innerHTML=[`<a href="${ROOT}">🏠 段考闖關</a>`].concat(parts).join(' ／ ')}
  fetch(ROOT+'catalog.json',{cache:'no-cache'}).then(r=>r.json()).then(cat=>{
    const levels=cat.levels.filter(l=>l.status!=='closed');
    if(!seg.length){
      h1.textContent='📚 段考闖關';sub.textContent='選學段開始：各校考卷統計＋真實照片動畫＋闖關練習＋交卷給老師';crumbs([]);
      hub.innerHTML=`<div class="grid">${levels.map(l=>card(ROOT+l.id+'/',l.name,l.status==='soon'?'':l.subjects.filter(s=>s.status==='open').map(s=>s.name).join('・'),l.emoji,l.color,shade(l.color,.35),'',l.status==='soon')).join('')}</div>`;
      return;
    }
    const L=cat.levels.find(l=>l.id===seg[0]);
    if(!L||L.status!=='open'){hub.innerHTML='<div class="msg">這個學段目前尚未開放。</div>';crumbs([]);return}
    if(seg.length===1){
      h1.textContent=`${L.emoji} ${L.name}段考闖關`;sub.textContent='選科目';crumbs([esc(L.name)]);
      const ss=L.subjects.filter(s=>s.status!=='closed');
      hub.innerHTML=ss.length?`<div class="grid">${ss.map(s=>card(ROOT+L.id+'/'+s.id+'/',s.name,s.status==='soon'?'':`${s.books.filter(b=>b.status==='open').length} 個闖關`,s.emoji,s.color,shade(s.color,.35),'',s.status==='soon')).join('')}</div>`:'<div class="msg">敬請期待。</div>';
      return;
    }
    const S=L.subjects.find(s=>s.id===seg[1]);
    if(!S||S.status!=='open'){hub.innerHTML='<div class="msg">這個科目目前暫停開放。</div>';crumbs([`<a href="${ROOT}${L.id}/">${esc(L.name)}</a>`]);return}
    h1.textContent=`${S.emoji} ${L.name}${S.name}段考闖關`;sub.textContent='選年級和學校用的版本';crumbs([`<a href="${ROOT}${L.id}/">${esc(L.name)}</a>`,esc(S.name)]);
    const books=S.books.filter(b=>b.status!=='closed'),grades=[...new Set(books.map(b=>b.grade))];
    hub.innerHTML=grades.map(g=>`<div class="grade">${esc(g)}</div><div class="grid">${books.filter(b=>b.grade===g).map(b=>{
        const [c1,c2]=VC[b.ver]||[S.color,shade(S.color,.35)];
        return card(ROOT+L.id+'/'+S.id+'/'+b.path+'/',`${b.grade}・${b.ver}`,b.desc,S.emoji,c1,c2,b.ver+'版',b.status==='soon')}).join('')}</div>`).join('')||'<div class="msg">敬請期待。</div>';
  }).catch(()=>{hub.innerHTML='<div class="msg">讀取選單失敗，請重新整理。</div>'});
})();
