// Test the Banner Connect help against real school questions (kb/tests/questions.json).
//   node kb/tests/run.js --search            the help box's article search, on the built site in public/ (run the build first)
//   node kb/tests/run.js --api <site url>    the help box's written answers (needs ANTHROPIC_API_KEY in that Vercel project)
// Exits with code 1 if anything fails.
const fs = require("fs"), path = require("path"), http = require("http");
const REPO = path.resolve(__dirname, "..", "..");
const T = JSON.parse(fs.readFileSync(path.join(__dirname, "questions.json"), "utf8"));
const mode = process.argv[2], target = process.argv[3];

function checkText(text, q) {
  const low = text.toLowerCase(), fails = [];
  for (const m of q.must || []) if (!m.split("|").some((alt) => low.includes(alt.toLowerCase()))) fails.push(`missing "${m}"`);
  for (const m of [...T.must_not_everywhere, ...(q.must_not || [])]) {
    const re = new RegExp(`\\b${m.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\b`, "i");
    if (re.test(text) && !(m === "GHL" && q.q.includes("GoHighLevel"))) fails.push(`mentions "${m}"`);
  }
  return fails;
}

async function viaApi() {
  let failed = 0;
  for (const q of T.questions) {
    const r = await fetch(target.replace(/\/$/, "") + "/api/help", { method: "POST", headers: { "content-type": "application/json", origin: target.replace(/\/$/, "") }, body: JSON.stringify({ question: q.q }) });
    if (!r.ok) { console.log(`FAIL  ${q.q}\n      HTTP ${r.status}${r.status === 503 ? " (no API key set in Vercel)" : ""}`); failed++; if (r.status === 503) break; continue; }
    const j = await r.json(), fails = checkText(j.answer || "", q);
    const src = (j.sources || []).map((s) => s.slug);
    if (q.article && !src.includes(q.article)) fails.push(`sources ${JSON.stringify(src)} don't include ${q.article}`);
    console.log(`${fails.length ? "FAIL" : "ok  "}  ${q.q}${fails.length ? "\n      " + fails.join("; ") : ""}`);
    if (fails.length) failed++;
  }
  return failed;
}

async function viaSearch() {
  const { chromium } = require("playwright");
  const PUB = path.join(REPO, "public");
  const server = http.createServer((req, res) => {
    let p = decodeURIComponent(req.url.split("?")[0]);
    if (p.startsWith("/api/")) { res.statusCode = 503; return res.end('{"error":"not_configured"}'); }
    if (p.endsWith("/")) p += "index.html";
    const f = path.join(PUB, p);
    if (!f.startsWith(PUB) || !fs.existsSync(f)) { res.statusCode = 404; return res.end(); }
    fs.createReadStream(f).pipe(res);
  }).listen(0);
  const port = server.address().port, browser = await chromium.launch(), page = await browser.newPage();
  await page.goto(`http://localhost:${port}/`);
  let failed = 0, first = 0, top3 = 0;
  for (const q of T.questions) {
    await page.fill("#ask-q", q.q);
    await page.click("#ask-form button");
    await page.waitForFunction(() => !document.querySelector(".a:last-child .dots"));
    const hits = await page.$$eval(".a:last-child .hit a", (as) => as.map((a) => a.getAttribute("href").split("/")[2]));
    const label = await page.$$eval(".a:last-child .hit", (hs) => hs.map((h) => h.querySelector("span").textContent + " > " + h.querySelector("b").textContent).join(" | "));
    if (!q.article) { console.log(`skip  ${q.q}`); continue; }
    const pos = hits.indexOf(q.article);
    if (pos === 0) first++;
    if (pos >= 0) top3++; else failed++;
    console.log(`${pos >= 0 ? "ok  " : "FAIL"}  ${q.q}\n      ${label || "(nothing found)"}`);
  }
  const n = T.questions.filter((q) => q.article).length;
  console.log(`\nRight article first: ${first} of ${n}. In the top three: ${top3} of ${n}.`);
  await browser.close(); server.close();
  return failed;
}

(async () => {
  if (mode === "--search") process.exitCode = (await viaSearch()) ? 1 : 0;
  else if (mode === "--api" && target) process.exitCode = (await viaApi()) ? 1 : 0;
  else { console.log("Usage: node kb/tests/run.js --search | --api https://demo.banner61.com"); process.exitCode = 2; }
})();
