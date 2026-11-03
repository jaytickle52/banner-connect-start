# Banner Connect: Getting Started and demos

Live at https://demo.banner61.com (demos at /demos/). The help site schools open from the Getting Started link in their Banner Connect menu, plus the clickable demo library at `/demos/`.

## Layout

- `site/content/getting-started.json`: the Getting Started page (first steps and the tab-by-tab menu guide)
- `site/content/guides/*.json`: one file per setup guide, published at `/help/<slug>/`
- `demos/tools/demos-src.json`: every demo, step by step (screenshot, hotspot, callout, cover-ups)
- `demos/raw/`: the original screen captures from the Banner Christian School demo account
- `demos/demos/library.json`: which demos show in the library, and which are "coming soon"
- `public/`: the built site. Vercel serves this folder as-is. Don't edit it by hand

## Update and publish

```
python3 demos/tools/build.py      # only after changing a demo or a capture (needs Pillow)
python3 site/tools/build_site.py  # rebuilds public/
git commit -am "..." && git push  # Vercel deploys main automatically
```
