"""Build the Banner Connect help site into dist/.

  python3 site/tools/build_site.py   (writes ../public)

Pages: /              Getting Started (content/getting-started.json)
       /help/<slug>/  one page per guide (content/guides/<slug>.json)
       /demos/        public copy of the clickable demo library
Styling matches the Banner Connect app (light, Inter, blue actions), branded Banner 61.
"""
import html, json, os, re, shutil, sys

import markdown
import yaml
from markdown.extensions.toc import slugify

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(ROOT)
DIST = os.path.join(REPO, "public")
KB_DIR = os.path.join(REPO, "kb")
API_KB = os.path.join(REPO, "api", "_kb.js")
DEMOS_SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, "demos")
e = html.escape

ICONS = {
    "gauge": '<path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/>',
    "sparkles": '<path d="M9.94 15.5A2 2 0 0 0 8.5 14.06l-6.14-1.58a.5.5 0 0 1 0-.96L8.5 9.94A2 2 0 0 0 9.94 8.5l1.58-6.14a.5.5 0 0 1 .96 0l1.58 6.14a2 2 0 0 0 1.44 1.44l6.14 1.58a.5.5 0 0 1 0 .96l-6.14 1.58a2 2 0 0 0-1.44 1.44l-1.58 6.14a.5.5 0 0 1-.96 0z"/>',
    "contacts": '<rect width="18" height="14" x="3" y="5" rx="2"/><circle cx="9" cy="11" r="2"/><path d="M6.5 16c.5-1.2 1.4-2 2.5-2s2 .8 2.5 2"/><path d="M14 10h4M14 14h3"/>',
    "calendar": '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "clipboard": '<rect width="8" height="4" x="8" y="2" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4M12 16h4M8 11h.01M8 16h.01"/>',
    "megaphone": '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    "workflow": '<rect width="8" height="8" x="3" y="3" rx="2"/><path d="M7 11v4a2 2 0 0 0 2 2h4"/><rect width="8" height="8" x="13" y="13" rx="2"/>',
    "chart": '<path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/>',
    "dollar": '<circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8M12 18V6"/>',
    "folder": '<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/>',
    "settings": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.93 4.93l2.12 2.12M16.95 16.95l2.12 2.12M2 12h3M19 12h3M4.93 19.07l2.12-2.12M16.95 7.05l2.12-2.12"/>',
    "play": '<path d="M6 4l14 8-14 8z"/>',
    "book": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "back": '<path d="M19 12H5M11 18l-6-6 6-6"/>',
    "help": '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3M12 17h.01"/>',
    "send": '<path d="m22 2-7 20-4-9-9-4z"/><path d="M22 2 11 13"/>',
}


def icon(name, size=18, cls="ic"):
    return (f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


CSS = """
:root{--bg:#f9fafb;--surface:#fff;--border:#eaecf0;--border-strong:#d0d5dd;--text:#101828;--body:#344054;--muted:#475467;--subtle:#667085;
--primary:#155eef;--primary-hover:#004eeb;--primary-50:#eff4ff;--primary-100:#d1e0ff;--success:#067647;--success-50:#ecfdf3;--success-200:#abefc6;
--warn-50:#fffaeb;--warn:#b54708;--b61:#ee5758;--font:"Inter",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color-scheme:light}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--body);font-family:var(--font);font-size:14px;line-height:1.5;
padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
a{color:var(--primary);text-decoration:none}a:hover{text-decoration:underline}
:focus-visible{outline:2px solid var(--primary);outline-offset:2px;border-radius:6px}
.page{max-width:1120px;margin:0 auto;padding-block:24px 48px;display:grid;grid-template-columns:minmax(0,1fr);gap:24px}
h1,h2,h3{color:var(--text);margin:0;text-wrap:balance}
h1{font-size:24px;line-height:32px;font-weight:600}
h2{font-size:18px;line-height:28px;font-weight:600}
h3{font-size:16px;line-height:24px;font-weight:600}
p{margin:0}
.head{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap}
.head p{color:var(--muted);max-width:68ch;margin-top:4px}
.brand{display:inline-flex;align-items:center;gap:8px;color:var(--subtle);font-size:12px;font-weight:500;white-space:nowrap}
.brand b{color:var(--text);font-weight:600}
.flag{width:18px;height:18px;display:inline-block;flex:none}
.card{background:var(--surface);border:1px solid var(--border);border-radius:12px;box-shadow:0 1px 2px rgba(16,24,40,.05)}
.card-head{padding:16px 20px;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.card-head p{color:var(--muted);font-size:13px}
.btn{display:inline-flex;align-items:center;gap:6px;height:36px;padding:0 14px;border-radius:8px;font-weight:600;font-size:14px;
border:1px solid var(--border-strong);background:var(--surface);color:var(--body);cursor:pointer;white-space:nowrap;font-family:inherit}
.btn:hover{background:var(--bg);text-decoration:none}
.btn.primary{background:var(--primary);border-color:var(--primary);color:#fff}.btn.primary:hover{background:var(--primary-hover)}
.btn .ic{flex:none}
.progress{display:flex;align-items:center;gap:10px;font-size:13px;color:var(--muted);font-variant-numeric:tabular-nums}
.bar{width:140px;height:8px;border-radius:99px;background:var(--border);overflow:hidden}
.bar i{display:block;height:100%;background:var(--primary);border-radius:99px;transition:width .3s}
.steps{list-style:none;margin:0;padding:0}
.step{display:grid;grid-template-columns:auto 1fr auto;gap:14px;align-items:center;padding:14px 20px;border-top:1px solid var(--border)}
.step:first-child{border-top:0}
.tick{width:24px;height:24px;border-radius:50%;border:1.5px solid var(--border-strong);background:var(--surface);display:grid;place-items:center;
cursor:pointer;color:transparent;padding:0}
.tick:hover{border-color:var(--primary)}
.step.done .tick{background:var(--primary);border-color:var(--primary);color:#fff}
.step.done .st{color:var(--subtle);text-decoration:line-through}
.st{font-weight:600;color:var(--text)}
.sb{color:var(--muted);font-size:13px}
.step>div{min-width:0}
.tabs-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:16px}
.tab{display:flex;flex-direction:column;padding:20px;gap:14px}
.tab-top{display:flex;align-items:center;gap:12px}
.tile{width:40px;height:40px;border-radius:10px;background:var(--primary-50);color:var(--primary);display:grid;place-items:center;flex:none}
.tab-top div{min-width:0}
.tab-top p{color:var(--muted);font-size:13px}
.pill{display:inline-block;font-size:12px;font-weight:500;padding:1px 8px;border-radius:99px;background:var(--warn-50);color:var(--warn);margin-left:6px;vertical-align:2px}
.inside{margin:0;display:grid;gap:8px}
.inside div{display:grid;grid-template-columns:132px 1fr;gap:12px;font-size:13px}
.inside dt{font-weight:500;color:var(--text)}
.inside dd{margin:0;color:var(--muted)}
.first{background:var(--bg);border-radius:8px;padding:10px 12px;font-size:13px;color:var(--body)}
.first b{color:var(--text);font-weight:600}
.links{margin-top:auto;display:flex;gap:8px;flex-wrap:wrap;padding-top:2px}
.foot{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;color:var(--subtle);font-size:13px;border-top:1px solid var(--border);padding-top:16px}
/* guide pages */
.crumb{display:inline-flex;align-items:center;gap:6px;color:var(--muted);font-weight:500;font-size:13px}
.meta{display:inline-flex;align-items:center;gap:6px;color:var(--subtle);font-size:13px;margin-top:8px}
.guide{max-width:760px;margin:0 auto;padding-block:24px 48px;display:grid;gap:20px}
.guide .lead{color:var(--muted);font-size:15px;max-width:65ch;margin-top:6px}
.gsteps{list-style:none;margin:0;padding:0;counter-reset:s}
.gstep{display:grid;grid-template-columns:32px 1fr;gap:14px;padding:18px 20px;border-top:1px solid var(--border)}
.gstep:first-child{border-top:0}
.num{width:28px;height:28px;border-radius:50%;background:var(--primary-50);color:var(--primary);font-weight:600;display:grid;place-items:center;font-size:13px}
.gstep p{color:var(--body);margin-top:2px;max-width:65ch}
.gstep div{min-width:0}
.ok{display:grid;grid-template-columns:auto 1fr;gap:12px;background:var(--success-50);border:1px solid var(--success-200);border-radius:12px;padding:16px 18px;color:var(--success)}
.ok b{display:block;color:#074d31;margin-bottom:2px}
.ok p{color:#085d3a}
.next{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:16px 20px;flex-wrap:wrap}
.next span{color:var(--subtle);font-size:12px;font-weight:500;text-transform:uppercase;letter-spacing:.04em}
/* ask a question */
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.ask-body{padding:16px 20px 20px;display:grid;gap:14px}
.ask-form{display:flex;gap:8px}
.ask-form input{flex:1;min-width:0;height:40px;border:1px solid var(--border-strong);border-radius:8px;padding:0 12px;font:inherit;font-size:15px;color:var(--text);background:var(--surface)}
.ask-form input:focus{outline:2px solid var(--primary-100);border-color:var(--primary)}
.ask-form .btn{height:40px}
.chips{display:flex;gap:8px;flex-wrap:wrap}
.chip{font:inherit;font-size:13px;color:var(--body);background:var(--bg);border:1px solid var(--border);border-radius:99px;padding:4px 12px;cursor:pointer}
.chip:hover{border-color:var(--primary);color:var(--primary)}
.thread{display:grid;gap:14px}
.thread:empty{display:none}
.q{justify-self:end;max-width:85%;background:var(--primary-50);color:var(--text);border-radius:12px 12px 4px 12px;padding:8px 12px;font-weight:500}
.a{border:1px solid var(--border);border-radius:12px;padding:14px 16px;display:grid;gap:10px;color:var(--body);max-width:72ch}
.a p,.a ol,.a ul{margin:0}.a ol,.a ul{padding-left:20px;display:grid;gap:4px}
.a b,.a strong{color:var(--text)}
.a .src{display:flex;gap:6px 12px;flex-wrap:wrap;font-size:13px;color:var(--subtle);border-top:1px solid var(--border);padding-top:10px}
.a .hit{display:grid;gap:2px}.a .hit+.hit{border-top:1px solid var(--border);padding-top:10px}
.a .hit span{font-size:12px;color:var(--subtle)}
.a .note{font-size:13px;color:var(--muted)}
.dots{display:inline-flex;gap:4px}.dots i{width:6px;height:6px;border-radius:50%;background:var(--subtle);animation:b 1s infinite ease-in-out}
.dots i:nth-child(2){animation-delay:.15s}.dots i:nth-child(3){animation-delay:.3s}
@keyframes b{0%,80%,100%{opacity:.25}40%{opacity:1}}
.ask-foot{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:13px;color:var(--subtle)}
.ask-foot button{font:inherit;color:var(--primary);background:none;border:0;padding:0;cursor:pointer}
.arts{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:4px 16px;margin:10px 0 0;padding:0;list-style:none;font-size:13px}
details.all summary{cursor:pointer;color:var(--primary);font-weight:500;font-size:13px}
/* article pages */
.prose{padding:20px 24px 24px;color:var(--body);font-size:15px;line-height:1.6}
.prose h2{font-size:18px;margin:24px 0 8px;scroll-margin-top:16px}
.prose h3{font-size:15px;margin:18px 0 6px}
.prose p,.prose ul,.prose ol{margin:0 0 12px;max-width:68ch}
.prose li{margin-bottom:4px}
.prose strong{color:var(--text)}
.prose>:first-child{margin-top:0}
.prose table{border-collapse:collapse;width:100%;font-size:14px;margin:0 0 16px;display:block;overflow-x:auto}
.prose th,.prose td{border:1px solid var(--border);padding:8px 10px;text-align:left;vertical-align:top}
.prose th{background:var(--bg);color:var(--text);font-weight:600}
.prose code{font-size:13px;background:var(--bg);border:1px solid var(--border);border-radius:4px;padding:0 4px}
@media (max-width:560px){.step{grid-template-columns:auto 1fr}.step .btn{grid-column:2;justify-self:start}.inside div{grid-template-columns:1fr;gap:0}}
@media (prefers-reduced-motion:reduce){.bar i{transition:none}.dots i{animation:none;opacity:.6}}
"""


def page(title, body, desc="", css_href="/assets/app.css"):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap">
<link rel="icon" href="/assets/favicon.png"><link rel="stylesheet" href="{css_href}">
<script>window.va=window.va||function(){{(window.vaq=window.vaq||[]).push(arguments)}};</script><script defer src="/_vercel/insights/script.js"></script></head><body>{body}</body></html>"""


def footer(support):
    return (f'<footer class="foot"><span class="brand"><img class="flag" src="/assets/banner61-mark.png" alt="" width="18" height="18"><b>Banner Connect</b> by Banner 61</span>'
            f'<a href="{e(support["href"])}" target="_blank" rel="noopener">{e(support["label"])}</a></footer>')


ASK_JS = r"""
(function(){
var form=document.getElementById("ask-form"),input=document.getElementById("ask-q"),thread=document.getElementById("ask-thread"),
reset=document.getElementById("ask-reset"),history=[],mode="ai",index=null;
function esc(s){return s.replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function inline(s){return esc(s).replace(/\*\*(.+?)\*\*/g,"<b>$1</b>").replace(/\[([^\]]+)\]\((\/help\/[^)\s]+)\)/g,'<a href="$2">$1</a>')}
function render(md){var out=[],list=null;md.replace(/\r/g,"").split("\n").forEach(function(l){var t=l.trim(),m;
if(!t){if(list){out.push("</"+list+">");list=null}return}
if((m=t.match(/^\d+[.)]\s+(.*)/))){if(list!=="ol"){if(list)out.push("</"+list+">");out.push("<ol>");list="ol"}out.push("<li>"+inline(m[1])+"</li>");return}
if((m=t.match(/^[-*]\s+(.*)/))){if(list!=="ul"){if(list)out.push("</"+list+">");out.push("<ul>");list="ul"}out.push("<li>"+inline(m[1])+"</li>");return}
if(list){out.push("</"+list+">");list=null}t=t.replace(/^#+\s*/,"");out.push("<p>"+inline(t)+"</p>")});
if(list)out.push("</"+list+">");return out.join("")}
var STOP="a an and are can do does for from get how i if in is it me my of on or our out set should the to up use we what when where which who why will with you your this that there have has".split(" ");
var SYN={staff:["user"],employee:["user"],assistant:["user"],teacher:["user"],access:["user","permission"],login:["sign"],password:["sign"],
family:["contact"],families:["contact"],parent:["contact"],parents:["contact"],tour:["visit"],tours:["visit"],book:["visit","calendar"],
open:["event"],house:["event"],text:["texting","sms"],texts:["texting","sms"],newsletter:["campaign"],deposit:["payment"],fee:["payment"],
pay:["payment"],website:["embed"],site:["embed"],field:["custom"],deleted:["restore"],accepted:["stage"],stage:["pipeline"],
followup:["workflow"],automation:["workflow"],automatic:["workflow"],email:["template"],wording:["template"],qr:["code"],
source:["report"],sources:["report"],report:["reporting"],facebook:["integrations"],instagram:["integrations"],notification:["notifications"],inquiry:["lead"],inquiries:["lead","report"],come:["source","report"],
heard:["activity","smart"],contacted:["activity","smart"],touch:["activity"],automatically:["workflow"],happens:["workflow"]};
function stem(w){return w.length>4?w.replace(/(ing|ed|es|s)$/,""):w}
function terms(q){var out=[];q.toLowerCase().replace(/[^a-z0-9 ]/g," ").split(/\s+/).forEach(function(w){if(!w||STOP.indexOf(w)>=0)return;
out.push(stem(w));(SYN[w]||[]).forEach(function(s){out.push(stem(s))})});return out}
function search(q){var ts=terms(q);if(!ts.length)return[];var N=index.length,df={};
index.forEach(function(s){s._w=s._w||(s.h+" "+s.x+" "+(s.k||"")).toLowerCase().replace(/[^a-z0-9 ]/g," ").split(/\s+/).map(stem);
s._hw=s._hw||s.h.toLowerCase().replace(/[^a-z0-9 ]/g," ").split(/\s+/).map(stem);
ts.forEach(function(t){if(s._w.indexOf(t)>=0)df[t]=(df[t]||0)+1})});
return index.map(function(s){var sc=0;ts.forEach(function(t){if(!df[t])return;var idf=Math.log(1+N/df[t]),c=0;
s._w.forEach(function(w){if(w===t)c++});if(c)sc+=idf*(1+Math.log(c));if(s._hw.indexOf(t)>=0)sc+=idf*2});return{s:s,sc:sc}})
.filter(function(r){return r.sc>0}).sort(function(a,b){return b.sc-a.sc}).slice(0,3).map(function(r){return r.s})}
function snippet(x){var p=x.split(/\n\s*\n/)[0].replace(/\*\*/g,"").replace(/\s+/g," ").trim();return p.length>280?p.slice(0,277).replace(/\s\S*$/,"")+"...":p}
function add(cls,html){var d=document.createElement("div");d.className=cls;d.innerHTML=html;thread.appendChild(d);return d}
function srcs(list){return list&&list.length?'<div class="src">From: '+list.map(function(s){return'<a href="help/articles/'+esc(s.slug)+'/">'+esc(s.title)+"</a>"}).join("")+"</div>":""}
function fallback(q,box){var go=function(){var hits=search(q);
box.innerHTML=hits.length?'<p class="note">Here\'s what our help articles say:</p>'+hits.map(function(s){return'<div class="hit"><span>'+esc(s.t)+'</span><a href="help/articles/'+esc(s.a)+"/#"+esc(s.id)+'"><b>'+esc(s.h)+"</b></a><p>"+esc(snippet(s.x))+"</p></div>"}).join("")
:"<p>I couldn't find that in our help articles. Try different words, or contact the Banner 61 team using the link at the bottom of this page.</p>";
if(window.va)window.va("event",{name:"Help search",found:hits.length?"yes":"no"})};
if(index)go();else fetch("assets/kb-index.json").then(function(r){return r.json()}).then(function(j){index=j;go()}).catch(function(){box.innerHTML="<p>Something went wrong. Please try again.</p>"})}
function ask(q){q=q.trim();if(!q)return;input.value="";add("q",esc(q));reset.hidden=false;
var box=add("a",'<span class="dots" aria-label="Working on it"><i></i><i></i><i></i></span>');box.scrollIntoView({block:"nearest"});
if(mode!=="ai")return fallback(q,box);
fetch("/api/help",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({question:q,history:history})})
.then(function(r){if(r.status===503)mode="search";if(!r.ok)throw r.status;return r.json()})
.then(function(j){box.innerHTML=render(j.answer||"")+srcs(j.sources);history.push({role:"user",content:q},{role:"assistant",content:j.answer||""});
history=history.slice(-6);if(window.va)window.va("event",{name:"Help answer"})})
.catch(function(s){if(s===429){box.innerHTML="<p>That's a lot of questions in a short time. Please wait a few minutes and try again.</p>";return}fallback(q,box)})}
form.addEventListener("submit",function(ev){ev.preventDefault();ask(input.value)});
[].forEach.call(document.querySelectorAll(".chip"),function(c){c.addEventListener("click",function(){ask(c.textContent)})});
reset.addEventListener("click",function(){thread.innerHTML="";history=[];reset.hidden=true;input.focus()});
})();
"""

ASK_EXAMPLES = ["How do I book a visit for a family who called?", "How do I give a new staff member access?",
                "How do I set up an open house?"]


def ask_section(kb):
    chips = "".join(f'<button class="chip" type="button">{e(q)}</button>' for q in ASK_EXAMPLES)
    arts = "".join(f'<li><a href="help/articles/{e(a["slug"])}/">{e(a["title"])}</a></li>' for a in kb)
    return f"""<section class="card" aria-labelledby="ask-h"><div class="card-head"><div><h2 id="ask-h">Ask a question</h2>
<p>Answers come from the Banner Connect help articles, written by the Banner 61 team for your account.</p></div></div>
<div class="ask-body"><form class="ask-form" id="ask-form"><label class="sr" for="ask-q">Your question</label>
<input id="ask-q" type="text" maxlength="600" autocomplete="off" placeholder="Ask how to do something in Banner Connect">
<button class="btn primary" type="submit">{icon("send",16)}Ask</button></form>
<div class="chips">{chips}</div>
<div class="thread" id="ask-thread" aria-live="polite"></div>
<div class="ask-foot"><details class="all"><summary>Browse all help articles</summary><ul class="arts">{arts}</ul></details>
<button type="button" id="ask-reset" hidden>Start over</button></div></div></section>"""


def build_index(gs, guides, demo_ids, kb):
    start_rows = []
    for s in gs["start"]:
        g = s.get("guide")
        btn = f'<a class="btn" href="help/{e(g)}/">{icon("book",16)}Open guide</a>' if g in guides else ""
        start_rows.append(f'<li class="step" data-id="{e(s["id"])}"><button class="tick" type="button" aria-pressed="false" '
                          f'aria-label="Mark done: {e(s["title"])}">{icon("check",14)}</button>'
                          f'<div><div class="st">{e(s["title"])}</div><div class="sb">{e(s["body"])}</div></div>{btn}</li>')
    cards = []
    for t in gs["tabs"]:
        pill = f'<span class="pill">{e(t["plan"])}</span>' if t.get("plan") else ""
        inside = "".join(f'<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>' for a, b in t["items"])
        links = []
        if t.get("demo") in demo_ids:
            links.append(f'<a class="btn primary" href="{e(gs.get("demosUrl","demos/"))}#{e(t["demo"])}" target="_blank" rel="noopener">{icon("play",14)}Watch the 1-minute demo</a>')
        if t.get("guide") in guides:
            links.append(f'<a class="btn" href="help/{e(t["guide"])}/">{icon("book",16)}Read the guide</a>')
        cards.append(f'<article class="card tab" id="{e(t["name"].lower().replace(" & ","-").replace(" ","-"))}">'
                     f'<div class="tab-top"><span class="tile">{icon(t["icon"],20)}</span><div><h3>{e(t["name"])}{pill}</h3>'
                     f'<p>{e(t["summary"])}</p></div></div><dl class="inside">{inside}</dl>'
                     f'<p class="first"><b>Try this first:</b> {e(t["first"])}</p>'
                     f'{"<div class=links>" + "".join(links) + "</div>" if links else ""}</article>')
    n = len(gs["start"])
    body = f"""<main class="page">
<header class="head"><div><h1>{e(gs["title"])}</h1><p>{e(gs["intro"])}</p></div>
<span class="brand"><img class="flag" src="/assets/banner61-mark.png" alt="" width="18" height="18"><b>Banner Connect</b> by Banner 61</span></header>
{ask_section(kb)}
<section class="card" aria-labelledby="start-h"><div class="card-head"><div><h2 id="start-h">Start here</h2><p>Four steps for your first week. Tick each one off as you go; your ticks are saved on this computer and browser only.</p></div>
<div class="progress"><span id="count">0 of {n} done</span><span class="bar"><i id="fill" style="width:0%"></i></span></div></div>
<ol class="steps">{"".join(start_rows)}</ol></section>
<section aria-labelledby="menu-h" style="display:grid;gap:12px"><div><h2 id="menu-h">Your menu, tab by tab</h2>
<p style="color:var(--muted)">What each tab in your menu is for, and the first thing to try.</p></div>
<div class="tabs-grid">{"".join(cards)}</div></section>
{footer(gs["support"])}</main>
<script>
(function(){{var KEY="bc-getting-started",done={{}};try{{done=JSON.parse(localStorage.getItem(KEY)||"{{}}")}}catch(_){{}}
var rows=[].slice.call(document.querySelectorAll(".step"));
function paint(){{var c=0;rows.forEach(function(r){{var on=!!done[r.dataset.id];r.classList.toggle("done",on);
r.querySelector(".tick").setAttribute("aria-pressed",on);if(on)c++}});
document.getElementById("count").textContent=c+" of "+rows.length+" done";document.getElementById("fill").style.width=(c/rows.length*100)+"%"}}
rows.forEach(function(r){{r.querySelector(".tick").addEventListener("click",function(){{done[r.dataset.id]=!done[r.dataset.id];
try{{localStorage.setItem(KEY,JSON.stringify(done))}}catch(_){{}}paint()}})}});paint()}})();
</script><script>{ASK_JS}</script>"""
    return page("Getting started", body, "Getting started with Banner Connect: first steps and what each menu tab is for.")


def build_guide(slug, g, guides, support):
    steps = "".join(f'<li class="gstep"><span class="num">{i}</span><div><h3>{e(s["title"])}</h3><p>{e(s["body"])}</p></div></li>'
                    for i, s in enumerate(g["steps"], 1))
    nxt = ""
    if g.get("next") in guides:
        n = guides[g["next"]]
        nxt = (f'<div class="card next"><div><span>Next step</span><h3>{e(n["title"])}</h3></div>'
               f'<a class="btn primary" href="../{e(g["next"])}/">Continue{icon("arrow",16)}</a></div>')
    body = f"""<main class="guide">
<a class="crumb" href="../../">{icon("back",16)}Getting started</a>
<header><h1>{e(g["title"])}</h1><p class="lead">{e(g["summary"])}</p>
<span class="meta">{icon("clock",14)}About {g["minutes"]} minutes</span></header>
<ol class="card gsteps">{steps}</ol>
<div class="ok">{icon("check",20)}<div><b>How to know it worked</b><p>{e(g["check"])}</p></div></div>
{nxt}{footer(support)}</main>"""
    return page(g["title"], body, g["summary"])


ASSISTANT_RULES = """## This assistant

You are the help assistant on the Getting Started page in Banner Connect. Staff type a question and you answer it.

- Answer only from the Banner Connect articles below. Don't use outside knowledge of other software, and never link to or mention any other website or help center.
- You can't see the school's account, families, numbers or settings, and you can't do anything in it. When someone asks about their own data (for example "which families haven't heard from us"), explain how to find it in Banner Connect, such as a Smart List filter or a report.
- If the articles don't cover the question, say that plainly in one sentence, give any closely related help the articles do cover, and suggest contacting the Banner 61 team with the "Contact Banner 61 support" link at the bottom of this page.
- If the question isn't about Banner Connect or school enrollment work, say you can only help with Banner Connect.
- Format: plain text with **bold** for menu names and buttons, numbered lists for steps, "- " bullets for options. No headings, no tables, no links. Aim for under 180 words.
- When one of these Getting Started guides or demos fits, mention it by name: {extras}.
- On the very last line, write SOURCES: followed by the ids of up to 3 articles you used, separated by commas (for example SOURCES: calendars, automations). Use the ids exactly as given. Write SOURCES: none if you used none."""


SITE = "https://demo.banner61.com"
META_KEYS = ("id", "title", "menu", "use_when", "also_called", "related", "reviewed")


def load_kb():
    """Read kb/NN-<id>.md. Each starts with a --- header block (see kb/README.md)."""
    arts = []
    for f in sorted(os.listdir(KB_DIR)):
        m = re.match(r"\d\d-(.+)\.md$", f)
        if not m:
            continue
        raw = open(os.path.join(KB_DIR, f)).read()
        hm = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
        if not hm:
            sys.exit(f"kb/{f}: missing the --- header block")
        meta = yaml.safe_load(hm.group(1)) or {}
        missing = [k for k in META_KEYS if not meta.get(k)]
        if missing:
            sys.exit(f"kb/{f}: header is missing {', '.join(missing)}")
        if meta["id"] != m.group(1):
            sys.exit(f"kb/{f}: id '{meta['id']}' must match the file name")
        text = raw[hm.end():].strip()
        lines = text.splitlines()
        title = lines[0].lstrip("#").strip()
        secs, cur = [], [title, []]
        for line in lines[1:]:
            if line.startswith("## "):
                secs.append(cur)
                cur = [line[3:].strip(), []]
            else:
                cur[1].append(line)
        secs.append(cur)
        sections = [(h, "\n".join(b).strip()) for h, b in secs if "\n".join(b).strip()]
        arts.append({"slug": meta["id"], "title": title, "text": text, "sections": sections, "meta": meta})
    ids = {a["slug"] for a in arts}
    for a in arts:
        bad = [r for r in a["meta"]["related"] if r not in ids]
        if bad:
            sys.exit(f"kb article {a['slug']}: related lists unknown ids {bad}")
    return arts


def absolute_links(text):
    return re.sub(r"\]\((/help/[^)\s]*)\)", lambda m: "](" + SITE + m.group(1) + ")", text)


def table_rows(s):
    """Markdown table -> 'cell: cell; cell' lines, header and divider rows dropped."""
    out, lines = [], s.splitlines()
    for i, l in enumerate(lines):
        if l.startswith("|"):
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if re.match(r"^\|?[-:| ]+\|?$", l) or re.match(r"^\|?[-:| ]+\|?$", nxt):
                continue
            cells = [c.strip() for c in l.strip("|").split("|")]
            out.append(cells[0] + ": " + "; ".join(cells[1:]))
        else:
            out.append(l)
    return "\n".join(out)


def strip_md(s):
    s = table_rows(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"^\s*(\d+\.|[-*])\s+", "", s, flags=re.M)
    s = re.sub(r"^\|?[-:| ]+\|?$", "", s, flags=re.M)
    return s.replace("|", " ").replace("`", "")


def build_kb(kb, guides, lib, support):
    index = []
    for a in kb:
        top = slugify(a["title"], "-")
        for h, body in a["sections"]:
            index.append({"a": a["slug"], "t": a["title"], "h": h, "id": top if h == a["title"] else slugify(h, "-"),
                          "x": strip_md(body), "k": " ".join(a["meta"]["also_called"])})
        body_md = "\n".join(a["text"].splitlines()[1:])
        content = markdown.markdown(body_md, extensions=["tables", "toc", "sane_lists"])
        others = "".join(f'<li><a href="../{e(o["slug"])}/">{e(o["title"])}</a></li>' for o in kb if o is not a)
        pg = f"""<main class="guide">
<a class="crumb" href="../../../">{icon("back",16)}Getting started</a>
<header><h1 id="{e(top)}">{e(a["title"])}</h1><span class="meta">{icon("book",14)}Banner Connect help · {e(a["meta"]["menu"])} · Reviewed {e(str(a["meta"]["reviewed"]))}</span></header>
<article class="card prose">{content}</article>
<div class="card" style="padding:16px 20px"><details class="all"><summary>More help articles</summary><ul class="arts">{others}</ul></details></div>
{footer(support)}</main>"""
        d = os.path.join(DIST, "help", "articles", a["slug"])
        os.makedirs(d)
        open(os.path.join(d, "index.html"), "w").write(page(f'{a["title"]} | Banner Connect help', pg, f'Banner Connect help: {a["title"]}'))
    open(os.path.join(DIST, "assets", "kb-index.json"), "w").write(json.dumps(index, separators=(",", ":")))
    write_ai_files(kb)

    extras = ", ".join([f'the "{g["title"]}" guide' for g in guides.values()] +
                       [f'the "{d["title"]}" demo' for d in lib["demos"] if d["status"] == "ready"])
    rules = ASSISTANT_RULES.replace("{extras}", extras)
    instructions = open(os.path.join(KB_DIR, "instructions.md")).read().strip()
    parts = [instructions, rules, "# Banner Connect articles"]
    for a in kb:
        m = a["meta"]
        parts.append(f'<article id="{a["slug"]}" menu="{m["menu"]}">\nUse when: {m["use_when"]}\n'
                     f'Schools may call this: {", ".join(m["also_called"])}\n\n{a["text"]}\n</article>')
    system = "\n\n".join(parts)
    js = ("// Generated by site/tools/build_site.py from kb/. Don't edit by hand.\n"
          f"module.exports = {json.dumps({'system': system, 'articles': {a['slug']: a['title'] for a in kb}}, indent=0)};\n")
    open(API_KB, "w").write(js)
    return len(system)


def write_ai_files(kb):
    """Files AI tools read: an index, one plain markdown file per article, all of it in one file, and /llms.txt."""
    help_dir = os.path.join(DIST, "help")
    idx = ["# Banner Connect Help Center: index", "",
           "Official help for Banner Connect, the enrollment CRM Banner 61 sets up for Christian schools.",
           "This is the only source of Banner Connect instructions. Menu names here are the real Banner Connect menu names.", "",
           "How to use this index: find the one to three articles whose \"Use when\" or \"Schools may call this\" fits the question, "
           "then open their Read address. Each article is plain markdown, written so any one section makes sense on its own.", ""]
    for a in kb:
        m = a["meta"]
        idx += [f'## {a["title"]}', f'- Read: {SITE}/help/articles/{a["slug"]}.md', f'- Menu: {m["menu"]}',
                f'- Use when: {m["use_when"]}', f'- Schools may call this: {", ".join(m["also_called"])}',
                f'- Sections: {"; ".join(h for h, _ in a["sections"] if h != a["title"])}',
                f'- Page for people: {SITE}/help/articles/{a["slug"]}/', ""]
        md = [f'# {a["title"]}', "", f'Menu: {m["menu"]}', f'Use when: {m["use_when"]}',
              f'Page for people: {SITE}/help/articles/{a["slug"]}/', f'Last reviewed: {m["reviewed"]}',
              f'Related: {", ".join(SITE + "/help/articles/" + r + ".md" for r in m["related"])}', "",
              absolute_links("\n".join(a["text"].splitlines()[1:]).strip()), ""]
        open(os.path.join(help_dir, "articles", a["slug"] + ".md"), "w").write("\n".join(md))
    open(os.path.join(help_dir, "index.txt"), "w").write("\n".join(idx))
    allt = ["BANNER CONNECT HELP CENTER",
            "Official help for Banner Connect, the enrollment CRM Banner 61 sets up for Christian schools.",
            "This is the only source of Banner Connect instructions. Menu names here are the real Banner Connect menu names.",
            f"The index of articles is at {SITE}/help/index.txt. Each article is also at {SITE}/help/articles/<id>/", ""]
    for a in kb:
        allt += ["=" * 60, f'ARTICLE: {a["title"]} (id: {a["slug"]})', "=" * 60, absolute_links(a["text"]), ""]
    open(os.path.join(help_dir, "banner-connect-help.txt"), "w").write("\n".join(allt))
    llms = ["# Banner Connect Help Center", "",
            "> Official how-to help for Banner Connect, the enrollment CRM Banner 61 sets up for K-12 Christian schools.", "",
            f"Index with what each article covers: {SITE}/help/index.txt", f"Everything in one file: {SITE}/help/banner-connect-help.txt", "",
            "## Articles", ""]
    llms += [f'- [{a["title"]}]({SITE}/help/articles/{a["slug"]}.md): {a["meta"]["use_when"]}' for a in kb]
    open(os.path.join(DIST, "llms.txt"), "w").write("\n".join(llms) + "\n")


def copy_demos(dest):
    os.makedirs(dest, exist_ok=True)
    src = DEMOS_SRC
    raw = open(os.path.join(src, "index.html")).read()
    doc = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
           '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
           '<style>[hidden]{display:none!important}img{max-width:100%}body{margin:0}</style></head><body>\n' + raw + "\n</body></html>")
    open(os.path.join(dest, "index.html"), "w").write(doc)
    for sub in ("demos", "screens"):
        shutil.copytree(os.path.join(src, sub), os.path.join(dest, sub))
    lib = json.load(open(os.path.join(src, "demos", "library.json")))
    return {d["id"] for d in lib["demos"] if d["status"] == "ready"}


def main():
    shutil.rmtree(DIST, ignore_errors=True)
    os.makedirs(DIST)
    gs = json.load(open(os.path.join(ROOT, "content", "getting-started.json")))
    gdir = os.path.join(ROOT, "content", "guides")
    guides = {f[:-5]: json.load(open(os.path.join(gdir, f))) for f in sorted(os.listdir(gdir)) if f.endswith(".json")}
    lib = json.load(open(os.path.join(DEMOS_SRC, "demos", "library.json")))
    demo_ids = {d["id"] for d in lib["demos"] if d["status"] == "ready"}
    if gs.get("demosUrl", "demos/") == "demos/":
        copy_demos(os.path.join(DIST, "demos"))
    os.makedirs(os.path.join(DIST, "assets"))
    for f in os.listdir(os.path.join(ROOT, "static")):
        shutil.copy(os.path.join(ROOT, "static", f), os.path.join(DIST, "assets", f))
    open(os.path.join(DIST, "assets", "app.css"), "w").write(" ".join(l.strip() for l in CSS.strip().splitlines()))
    kb = load_kb()
    open(os.path.join(DIST, "index.html"), "w").write(build_index(gs, guides, demo_ids, kb))
    for slug, g in guides.items():
        d = os.path.join(DIST, "help", slug)
        os.makedirs(d)
        open(os.path.join(d, "index.html"), "w").write(build_guide(slug, g, guides, gs["support"]))
    size = build_kb(kb, guides, lib, gs["support"])
    print("built:", len(guides), "guides,", len(demo_ids), "demos,", len(kb), f"help articles (assistant prompt {size:,} characters)")


if __name__ == "__main__":
    main()
