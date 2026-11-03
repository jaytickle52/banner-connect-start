// POST /api/help  {question, history?}  ->  {answer, sources}
// Answers Banner Connect how-to questions from our own knowledge base (kb/), never the web.
// Needs ANTHROPIC_API_KEY in the Vercel project's environment variables. Without it this
// returns 503 and the Getting Started page falls back to searching the articles itself.
// Optional: HELP_MODEL (default claude-haiku-5-5).
const KB = require("./_kb.js");

const ALLOWED = [/^https:\/\/demo\.banner61\.com$/, /^https:\/\/[a-z0-9-]+\.vercel\.app$/, /^http:\/\/localhost(:\d+)?$/];
const hits = new Map(); // best-effort, per instance: 20 questions per IP per 10 minutes
const WINDOW = 10 * 60 * 1000, LIMIT = 20;

function limited(ip) {
  const now = Date.now();
  const list = (hits.get(ip) || []).filter((t) => now - t < WINDOW);
  list.push(now);
  hits.set(ip, list);
  return list.length > LIMIT;
}

function clean(s, max) {
  return String(s || "").replace(/\s+/g, " ").trim().slice(0, max);
}

module.exports = async (req, res) => {
  if (req.method !== "POST") return res.status(405).json({ error: "method_not_allowed" });
  const origin = req.headers.origin || "";
  if (origin && !ALLOWED.some((r) => r.test(origin))) return res.status(403).json({ error: "forbidden" });
  const key = process.env.ANTHROPIC_API_KEY;
  if (!key) return res.status(503).json({ error: "not_configured" });
  const ip = String(req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "unknown";
  if (limited(ip)) return res.status(429).json({ error: "rate_limited" });

  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch (_) { body = {}; } }
  const question = clean(body && body.question, 600);
  if (!question) return res.status(400).json({ error: "empty_question" });

  const history = Array.isArray(body.history) ? body.history.slice(-6) : [];
  const messages = [];
  for (const m of history) {
    const role = m && m.role === "assistant" ? "assistant" : "user";
    const content = clean(m && m.content, 2000);
    if (!content) continue;
    if (messages.length && messages[messages.length - 1].role === role) continue;
    if (!messages.length && role !== "user") continue;
    messages.push({ role, content });
  }
  if (messages.length && messages[messages.length - 1].role === "user") messages.pop();
  messages.push({ role: "user", content: question });

  try {
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json" },
      body: JSON.stringify({
        model: process.env.HELP_MODEL || "claude-haiku-5-5",
        max_tokens: 900,
        system: [{ type: "text", text: KB.system, cache_control: { type: "ephemeral" } }],
        messages,
      }),
    });
    if (!r.ok) {
      console.error("anthropic", r.status, (await r.text()).slice(0, 500));
      return res.status(502).json({ error: "upstream" });
    }
    const data = await r.json();
    let text = (data.content || []).filter((b) => b.type === "text").map((b) => b.text).join("\n").trim();
    let sources = [];
    const m = text.match(/\n?SOURCES:\s*(.*)\s*$/i);
    if (m) {
      text = text.slice(0, m.index).trim();
      sources = m[1].split(/[,\s]+/).map((s) => s.trim()).filter((s) => KB.articles[s])
        .slice(0, 3).map((s) => ({ slug: s, title: KB.articles[s] }));
    }
    return res.status(200).json({ answer: text, sources });
  } catch (err) {
    console.error(err);
    return res.status(502).json({ error: "upstream" });
  }
};
