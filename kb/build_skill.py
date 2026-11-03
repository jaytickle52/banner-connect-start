#!/usr/bin/env python3
"""Bundle the Banner Connect knowledge base into Ask AI skill files.

Usage: python3 kb/build_skill.py
Writes one SKILL.md per group in kb/dist/<skill-name>/SKILL.md.
Each skill = the shared answering instructions + its articles.
Ask AI limits: name 80 characters, description 500, instructions 50,000.
"""
from pathlib import Path

KB = Path(__file__).resolve().parent
DIST = KB / "dist"
LIMIT = 50_000

GROUPS = [
    {
        "name": "banner-connect-help-crm",
        "description": "Use for how-to questions about Banner Connect basics: signing in, the menu, first setup steps, contacts, tags, smart lists, imports, the enrollment pipeline and opportunities, conversations, snippets, texting, tasks and task notifications.",
        "articles": ["00", "01", "02", "03", "04", "05"],
    },
    {
        "name": "banner-connect-help-visits-forms",
        "description": "Use for how-to questions about Banner Connect calendars, campus visits, open houses and event registration, booking for a family, forms, putting a form on the school website, surveys, and documents and contracts families sign.",
        "articles": ["00", "06", "07"],
    },
    {
        "name": "banner-connect-help-marketing-automation",
        "description": "Use for how-to questions about Banner Connect email templates, email campaigns, trigger links, funnels, QR codes, social planner, automations and workflows, the dashboard, reporting, payments, custom fields, custom values, merge fields, users and settings.",
        "articles": ["00", "08", "09", "10", "11"],
    },
]


def demote(text):
    return "\n".join(("#" + l) if l.startswith("#") else l for l in text.strip().splitlines())


def main():
    instructions = (KB / "instructions.md").read_text().strip()
    for g in GROUPS:
        parts = [instructions, "# Banner Connect articles"]
        for prefix in g["articles"]:
            (path,) = KB.glob(f"{prefix}-*.md")
            parts.append(demote(path.read_text()))
        body = "\n\n".join(parts).rstrip() + "\n"
        assert len(g["name"]) <= 80 and len(g["description"]) <= 500
        assert len(body) <= LIMIT, f"{g['name']} is {len(body)} characters, over {LIMIT}"
        out = DIST / g["name"]
        out.mkdir(parents=True, exist_ok=True)
        front = f"---\nname: {g['name']}\ndescription: {g['description']}\n---\n\n"
        (out / "SKILL.md").write_text(front + body)
        (out / "body.md").write_text(body)  # instructions only, for pasting into Ask AI's form
        print(f"{g['name']}: {len(body):,} characters")


if __name__ == "__main__":
    main()
