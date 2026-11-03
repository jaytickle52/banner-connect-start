"""Build the Banner Connect help site into dist/.

  python3 site/tools/build_site.py   (writes ../public)

Pages: /              Getting Started (content/getting-started.json)
       /help/<slug>/  one page per guide (content/guides/<slug>.json)
       /demos/        public copy of the clickable demo library
Styling matches the Banner Connect app (light, Inter, blue actions), branded Banner 61.
"""
import html, json, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(ROOT)
DIST = os.path.join(REPO, "public")
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
.page{max-width:1120px;margin:0 auto;padding-block:24px 48px;display:grid;gap:24px}
h1,h2,h3{color:var(--text);margin:0;text-wrap:balance}
h1{font-size:24px;line-height:32px;font-weight:600}
h2{font-size:18px;line-height:28px;font-weight:600}
h3{font-size:16px;line-height:24px;font-weight:600}
p{margin:0}
.head{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap}
.head p{color:var(--muted);max-width:68ch;margin-top:4px}
.brand{display:inline-flex;align-items:center;gap:8px;color:var(--subtle);font-size:12px;font-weight:500;white-space:nowrap}
.brand b{color:var(--text);font-weight:600}
.flag{width:8px;height:14px;background:var(--b61);clip-path:polygon(0 0,100% 0,100% 100%,50% 75%,0 100%);display:inline-block}
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
@media (max-width:560px){.step{grid-template-columns:auto 1fr}.step .btn{grid-column:2;justify-self:start}.inside div{grid-template-columns:1fr;gap:0}}
@media (prefers-reduced-motion:reduce){.bar i{transition:none}}
"""


def page(title, body, desc="", css_href="/assets/app.css"):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{css_href}"></head><body>{body}</body></html>"""


def footer(support):
    return (f'<footer class="foot"><span class="brand"><span class="flag"></span><b>Banner Connect</b> by Banner 61</span>'
            f'<a href="{e(support["href"])}" target="_blank" rel="noopener">{e(support["label"])}</a></footer>')


def build_index(gs, guides, demo_ids):
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
<span class="brand"><span class="flag"></span><b>Banner Connect</b> by Banner 61</span></header>
<section class="card" aria-labelledby="start-h"><div class="card-head"><div><h2 id="start-h">Start here</h2><p>Four steps for your first week.</p></div>
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
</script>"""
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


def copy_demos(dest):
    os.makedirs(dest, exist_ok=True)
    src = DEMOS_SRC
    raw = open(os.path.join(src, "index.html")).read()
    doc = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
           '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
           '<style>[hidden]{display:none!important}img{max-width:100%}body{margin:0}</style></head><body>\n' + raw + "\n</body></html>")
    open(os.path.join(dest, "index.html"), "w").write(doc)
    for sub in ("demos", "screens", "assets"):
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
    open(os.path.join(DIST, "assets", "app.css"), "w").write(" ".join(l.strip() for l in CSS.strip().splitlines()))
    open(os.path.join(DIST, "index.html"), "w").write(build_index(gs, guides, demo_ids))
    for slug, g in guides.items():
        d = os.path.join(DIST, "help", slug)
        os.makedirs(d)
        open(os.path.join(d, "index.html"), "w").write(build_guide(slug, g, guides, gs["support"]))
    print("built:", len(guides), "guides,", len(demo_ids), "demos")


if __name__ == "__main__":
    main()
