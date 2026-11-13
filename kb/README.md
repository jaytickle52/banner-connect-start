# Banner Connect help articles

This folder is the one master copy of Banner Connect help. Everything else is built from it on every push to main:

| Built from kb/ | Address | Who reads it |
|---|---|---|
| Article pages | demo.banner61.com/help/articles/&lt;id&gt;/ | School staff |
| "Ask a question" box | demo.banner61.com (top of Getting Started) | School staff |
| Index | demo.banner61.com/help/index.txt | Ask AI and other AI tools (read first) |
| One file per article | demo.banner61.com/help/articles/&lt;id&gt;.md | Ask AI and other AI tools |
| Everything in one file | demo.banner61.com/help/banner-connect-help.txt | Backup for AI tools |
| llms.txt | demo.banner61.com/llms.txt | AI tools that look for it |

Don't edit anything in `public/` or `api/_kb.js` by hand. Change the article here and push.

## Change an article

1. Open the file in GitHub (github.com/jaytickle52/banner-connect-start, folder `kb/`) and click the pencil.
2. Make the change. Update `reviewed:` to today's date.
3. Commit to main. The site rebuilds in about a minute.

Or send a Base Camp task to Claude: "In the Banner Connect help, change the calendars article to say ..."

## Add an article

Name it `NN-<id>.md`, where NN sets the order and `<id>` is short, lowercase and never changes once published (links point to it). Copy this:

```
---
id: open-houses
title: "Open houses"
menu: "Calendars > Meeting Calendars"
use_when: "One or two sentences on the questions this answers, in school words."
also_called: ["open house", "preview day", "information night", "RSVP"]
related: [calendars, automations]
plan: ""  # SchoolBox, Full or All
reviewed: 2026-11-03
---
# Open houses

One or two sentences on what this is and where it lives.

## Set up an open house

The first sentence answers the question. Then the steps:

1. Go to **Calendars**, then **Meeting Calendars**.
2. ...

How to check it worked: ...
```

The build stops with a message if the header is missing a field, the id doesn't match the file name, or `related` names an article that doesn't exist.

## How to write so the AI gets it right

- **Headings are tasks or questions, in school words.** A how-to section is named for the task: "Book a visit for a family who called", not "Appointments". An explainer section is named for the question staff actually ask: "What is a smart list?", "Why is this family on Stalled Leads?". Never a bare feature name.
- **The first sentence of each section answers the question.** In a how-to section, then numbered steps, then "How to check it worked." In an explainer, a few plain sentences that answer it, then a link to the how-to section that goes with it. No steps and no "How to check it worked" in an explainer.
- **Every section stands on its own.** The AI often reads one section without the rest. Repeat the menu path in each section. Never write "as above", "see below" or "the previous step". To point elsewhere, link to the section: `[Connect your calendar](/help/articles/calendars/#connect-your-calendar)`.
- **Exact menu names, in bold, with "then":** **Advanced**, then **Custom Fields**. Not "Settings > Custom Fields" or "the fields page".
- **Exact account names** from the "Names in your account" section of `00-about-banner-connect.md`: Request Info Packet, Schedule a Visit, Event Registration, Inquiry to Enrollment, Current Families. If you add a form, calendar, stage or workflow, add it there too.
- **`also_called` is the most important line in the header.** It's the words schools actually type: "tour" for a visit, "newsletter" for a campaign, "staff" for a user. Most wrong answers in the Nov 3 test came from this mismatch. When a school asks something in words that aren't listed, add them.
- **Flag the risky changes.** Wherever a change could break workflows, stages, tags, fields, texting, email sending or payments, say to check with the Banner 61 team first. The AI repeats that warning.
- **Never mention other software or other help sites.** The product is Banner Connect. The mobile app is LeadConnector.
- **No information only in a screenshot.** The AI can't see images. Say it in words.
- **No em dashes.**

## Test after changes

`kb/tests/questions.json` holds real school questions with what a good answer must and must not say. Run:

```
python3 site/tools/build_site.py
node kb/tests/run.js --search                          # the help box's article search (no API key needed)
node kb/tests/run.js --api https://demo.banner61.com   # the help box's written answers (needs the API key in Vercel)
```

To test Ask AI, ask Claude: "rerun the Banner Connect help questions in Ask AI." When a school asks something the help gets wrong, add it to `questions.json`.
