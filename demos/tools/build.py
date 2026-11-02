"""Build the Banner Connect demo library from tools/demos-src.json and raw/ captures.

Run from the project folder:  python3 tools/build.py
Writes screens/<demo-id>/NN.jpg and demos/<demo-id>.json. Edit the source file, not the outputs.
"""
import json, os, shutil
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = json.load(open(os.path.join(ROOT, "tools", "demos-src.json")))
CW, CH = SRC["canvas"]
FONTS = "/usr/share/fonts/opentype/inter/Inter-{}.otf"


def font(weight, size):
    try:
        return ImageFont.truetype(FONTS.format(weight), size)
    except OSError:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)


def apply_edits(im, edits):
    d = ImageDraw.Draw(im)
    for e in edits or []:
        if e["type"] == "fill":
            d.rectangle(e["box"], fill=e["color"])
        elif e["type"] == "text":
            d.text(tuple(e["at"]), e["text"], fill=e.get("color", "#1d2433"),
                   font=font(e.get("weight", "Regular"), e.get("size", 13)))
        elif e["type"] == "badge":  # neutral round crest in place of a logo
            x0, y0, x1, y1 = e["box"]
            d.rectangle(e["box"], fill="#ffffff")
            d.ellipse(e["box"], fill="#1f3a5f")
            f = font("Bold", int((y1 - y0) * 0.3))
            w = d.textlength(e["text"], font=f)
            d.text(((x0 + x1 - w) / 2, (y0 + y1) / 2 - (y1 - y0) * 0.19), e["text"], fill="#ffffff", font=f)
    return im


def fit(im):
    """Scale a capture onto the fixed canvas, padding with its own edge colors."""
    w, h = im.size
    s = min(CW / w, CH / h)
    nw, nh = round(w * s), round(h * s)
    ox, oy = (CW - nw) // 2, (CH - nh) // 2
    canvas = Image.new("RGB", (CW, CH), im.getpixel((w - 2, h // 2)))
    if ox:
        canvas.paste(im.getpixel((1, h // 2)), (0, 0, ox, CH))
    canvas.paste(im.resize((nw, nh), Image.LANCZOS), (ox, oy))
    return canvas, s, ox, oy


def main():
    for demo in SRC["demos"]:
        out_dir = os.path.join(ROOT, "screens", demo["id"])
        shutil.rmtree(out_dir, ignore_errors=True)
        os.makedirs(out_dir)
        steps = []
        for i, st in enumerate(demo["steps"], 1):
            im = Image.open(os.path.join(ROOT, "raw", st["raw"])).convert("RGB")
            im = apply_edits(im, st.get("edits"))
            im, s, ox, oy = fit(im)
            name = f"{i:02d}.jpg"
            im.save(os.path.join(out_dir, name), quality=86, optimize=True)
            x0, y0, x1, y1 = st["hotspot"]
            pct = lambda v, o, tot: round((v * s + o) / tot * 100, 2)
            steps.append({
                "image": f"screens/{demo['id']}/{name}",
                "alt": st["alt"],
                "illustration": st.get("illustration", False),
                "hotspot": {"x": pct(x0, ox, CW), "y": pct(y0, oy, CH),
                            "w": round((x1 - x0) * s / CW * 100, 2), "h": round((y1 - y0) * s / CH * 100, 2)},
                "title": st["title"], "body": st["body"], "hint": st["hint"],
            })
        out = {"id": demo["id"], "title": demo["title"], "school": SRC["school"],
               "aspect": f"{CW} / {CH}", "start": demo["start"], "steps": steps, "finish": demo["finish"]}
        json.dump(out, open(os.path.join(ROOT, "demos", demo["id"] + ".json"), "w"), indent=2)
        print(demo["id"], len(steps), "steps")


if __name__ == "__main__":
    main()
