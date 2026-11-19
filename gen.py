#!/usr/bin/env python3
"""
The Global Ledger - Thursday 19 November 2026.
One-page world-news poster for the make.fun news-image-20261119 contest.

The picture is drawn entirely in code with PIL: a light newspaper
masthead, a region count bar, a day-in-numbers strip, three illustrated
lead stories, ten illustrated grid stories, a flat world map with the
thirteen illustrated stories pinned on it, an ALSO column list of
twenty-seven more stories, a DATE CHECK box naming the tempting stories
that were left out because they were first reported on 18 November or
earlier, and a footer attestation.  Every story happened, or was first
reported, on Thursday 19 November 2026.

Layout and the paint() interpreter are data-driven: each story carries
its headline, deck, kicker, region, map pin and a list of paint ops, so
the page is a rendering of the data below, nothing else.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 26
PAGE_W = W - 2 * MARGIN

PAPER = (247, 243, 233)
INK = (26, 24, 20)
MUTE = (96, 90, 80)
RULE = (40, 38, 34)
ACCENT = (178, 30, 40)
CREAM = (255, 253, 247)
CHIP_BG = (24, 24, 26)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def tracked_text(draw, x, y, text, fnt, fill, step=2):
    """Draw letterspaced text starting at x; return the end x."""
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=fnt, fill=fill)
        cx += draw.textlength(ch, font=fnt) + step
    return cx


def tracked_width(draw, text, fnt, step=2):
    return sum(draw.textlength(ch, font=fnt) + step for ch in text) - step


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def chip_text(draw, x, y, text, fnt, fill, bg, pad_x=7, pad_y=3):
    """Small filled label with text; returns its width."""
    tw = draw.textlength(text, font=fnt)
    th = fnt.size
    draw.rectangle([x, y, x + tw + 2 * pad_x, y + th + 2 * pad_y], fill=bg)
    draw.text((x + pad_x, y + pad_y - 1), text, font=fnt, fill=fill)
    return tw + 2 * pad_x


# ---------------------------------------------------------------- paint ops
# A scene is a list of ops drawn inside a box (x0, y0, w, h).  Coordinates
# in the ops are fractions of the box unless the op says otherwise.

def paint(draw, box, ops):
    x0, y0, w, h = box

    def px(fx):
        return x0 + fx * w

    def py(fy):
        return y0 + fy * h

    for op in ops:
        kind = op[0]
        if kind == "bg":
            draw.rectangle([x0, y0, x0 + w, y0 + h], fill=op[1])
        elif kind == "rect":
            _, fx, fy, fw, fh, col = op
            draw.rectangle([px(fx), py(fy), px(fx + fw), py(fy + fh)], fill=col)
        elif kind == "rrect":
            _, fx, fy, fw, fh, col = op
            draw.rounded_rectangle(
                [px(fx), py(fy), px(fx + fw), py(fy + fh)],
                radius=min(w * fw, h * fh) * 0.28, fill=col)
        elif kind == "line":
            _, ax, ay, bx, by, col = op[:6]
            wd = op[6] if len(op) > 6 else 2
            draw.line([px(ax), py(ay), px(bx), py(by)], fill=col, width=wd)
        elif kind == "dashed":
            _, ax, ay, bx, by, col = op
            steps = 26
            for i in range(0, steps, 2):
                t1, t2 = i / steps, (i + 1) / steps
                draw.line([px(ax + (bx - ax) * t1), py(ay + (by - ay) * t1),
                           px(ax + (bx - ax) * t2), py(ay + (by - ay) * t2)],
                          fill=col, width=2)
        elif kind == "arrow":
            _, ax, ay, bx, by, col = op
            draw.line([px(ax), py(ay), px(bx), py(by)], fill=col, width=3)
            draw.polygon([(px(bx), py(by)), (px(bx - 0.045), py(by - 0.10)),
                          (px(bx + 0.005), py(by + 0.055))], fill=col)
        elif kind == "circle":
            _, cx, cy, r, col = op
            rr = r * w
            draw.ellipse([px(cx) - rr, py(cy) - rr * h / w,
                          px(cx) + rr, py(cy) + rr * h / w], fill=col)
        elif kind == "poly":
            _, pts, col = op
            draw.polygon([(px(a), py(b)) for a, b in pts], fill=col)
        elif kind == "polyline":
            _, pts, col = op[:3]
            wd = op[3] if len(op) > 3 else 3
            draw.line([(px(a), py(b)) for a, b in pts], fill=col, width=wd,
                      joint="curve")
        elif kind == "text":
            _, cx, fy, txt, size, col = op
            fnt = font(SANS_B, size)
            tw = draw.textlength(txt, font=fnt)
            draw.text((px(cx) - tw / 2, py(fy)), txt, font=fnt, fill=col)
        elif kind == "person":
            _, cx, fy, s, skin, cloth = op
            head_r = s * h * 0.24
            hcy = py(fy) + s * h * 0.26
            draw.ellipse([px(cx) - head_r, hcy - head_r,
                          px(cx) + head_r, hcy + head_r], fill=skin)
            shw = s * h * 0.55 / w
            draw.polygon([(px(cx - shw), py(fy + s)),
                           (px(cx - shw * 0.72), py(fy + s * 0.55)),
                           (px(cx + shw * 0.72), py(fy + s * 0.55)),
                           (px(cx + shw), py(fy + s))], fill=cloth)
        elif kind == "flag":
            _, fx, fy, fw, fh, which = op
            pole_x = px(fx)
            draw.line([pole_x, py(fy), pole_x, py(fy + fh * 2.1)],
                      fill=(210, 210, 215), width=2)
            fx0, fy0, fx1, fy1 = px(fx), py(fy), px(fx + fw), py(fy + fh)
            if which == "us":
                draw.rectangle([fx0, fy0, fx1, fy1], fill=(178, 34, 52))
                for i in range(1, 6, 2):
                    sy = fy0 + (fy1 - fy0) * i / 6
                    draw.rectangle([fx0, sy, fx1, sy + (fy1 - fy0) / 6],
                                   fill=(240, 240, 240))
                draw.rectangle([fx0, fy0, fx0 + (fx1 - fx0) * 0.45,
                                fy0 + (fy1 - fy0) * 0.55], fill=(30, 40, 110))
            elif which == "cn":
                draw.rectangle([fx0, fy0, fx1, fy1], fill=(206, 40, 40))
                for dx, dy in ((0.16, 0.28), (0.34, 0.16), (0.38, 0.36),
                               (0.34, 0.55)):
                    rr = (fx1 - fx0) * 0.055
                    cxp, cyp = fx0 + (fx1 - fx0) * dx, fy0 + (fy1 - fy0) * dy
                    draw.ellipse([cxp - rr, cyp - rr, cxp + rr, cyp + rr],
                                 fill=(250, 210, 60))
            elif which == "ru":
                third = (fy1 - fy0) / 3
                draw.rectangle([fx0, fy0, fx1, fy0 + third],
                               fill=(240, 240, 240))
                draw.rectangle([fx0, fy0 + third, fx1, fy0 + 2 * third],
                               fill=(30, 60, 160))
                draw.rectangle([fx0, fy0 + 2 * third, fx1, fy1],
                               fill=(200, 40, 40))
        elif kind == "building":
            _, fx, fy, fw, fh, col = op
            draw.rectangle([px(fx), py(fy), px(fx + fw), py(fy + fh)], fill=col)
            draw.line([px(fx), py(fy), px(fx + fw), py(fy)], fill=col, width=3)
        elif kind == "buildings":
            _, fx, fy, fw, fh, col = op
            heights = (0.62, 0.9, 0.5, 1.0, 0.7, 0.85, 0.55, 0.95, 0.66, 0.8)
            n = len(heights)
            bw = fw / n
            for i, hf in enumerate(heights):
                bx = fx + i * bw
                draw.rectangle([px(bx), py(fy + fh * (1 - hf)),
                                px(bx + bw * 0.88), py(fy + fh)], fill=col)
                for r in range(3):
                    for c in range(2):
                        if (i * 7 + r * 3 + c) % 3 == 0:
                            wx = px(bx + bw * (0.18 + c * 0.36))
                            wy = py(fy + fh * (1 - hf) + fh * (0.16 + r * 0.24))
                            draw.rectangle([wx, wy, wx + 2.4, wy + 3.2],
                                           fill=(250, 214, 130))
        elif kind == "crowd":
            _, fx, fy, fw, fh, col = op
            rows = 3
            for r in range(rows):
                yy = fy - fh * (r / rows) * 0.62
                count = 9 - r
                for i in range(count):
                    cx = fx + fw * (i + 0.5 + (r % 2) * 0.4) / count
                    hr = fh * h * 0.16
                    draw.ellipse([px(cx) - hr, py(yy) - fh * h * 0.30,
                                  px(cx) + hr, py(yy) - fh * h * 0.30 + 2 * hr],
                                 fill=col)
                    draw.rectangle([px(cx) - hr * 1.5, py(yy) - fh * h * 0.12,
                                    px(cx) + hr * 1.5, py(yy) + 2], fill=col)
        elif kind == "bar":
            _, fx, fy, fw, fh, col = op
            draw.rectangle([px(fx), py(fy - fh), px(fx + fw), py(fy)], fill=col)
        elif kind == "bars":
            _, fx, fy, heights, fw, col = op
            n = len(heights)
            bw = fw / n
            for i, hf in enumerate(heights):
                bx = fx + i * bw
                draw.rectangle([px(bx), py(fy - hf), px(bx + bw * 0.7), py(fy)],
                               fill=col)
        elif kind == "dots":
            _, fx, fy, fw, fh, rows, col = op
            cols = max(2, int(fw / fh * rows * 1.6))
            for r in range(rows):
                for c in range(cols):
                    if (r * 5 + c * 3) % 4 == 1:
                        continue
                    cx = px(fx + fw * (c + 0.5) / cols)
                    cy = py(fy + fh * (r + 0.5) / rows)
                    draw.ellipse([cx - 1.8, cy - 1.8, cx + 1.8, cy + 1.8],
                                 fill=col)
        elif kind == "tank":
            _, cx, fy, s, col = op
            draw.rectangle([px(cx - s * 0.5), py(fy - s * 0.30),
                            px(cx + s * 0.42), py(fy)], fill=col)
            draw.rectangle([px(cx - s * 0.18), py(fy - s * 0.48),
                            px(cx + s * 0.16), py(fy - s * 0.30)], fill=col)
            draw.line([px(cx + s * 0.10), py(fy - s * 0.42),
                       px(cx + s * 0.62), py(fy - s * 0.50)], fill=col, width=4)
            for i in range(4):
                wx = px(cx - s * 0.40 + i * s * 0.24)
                draw.ellipse([wx, py(fy) - 4, wx + 7, py(fy) + 3],
                             fill=(30, 30, 28))
        elif kind == "globe":
            _, cx, cy, r = op
            rr = r * w
            cyx = py(cy)
            draw.ellipse([px(cx) - rr, cyx - rr, px(cx) + rr, cyx + rr],
                         fill=(52, 110, 140))
            blobs = ((-0.45, -0.30, 0.30), (-0.10, -0.52, 0.22),
                     (0.30, -0.28, 0.34), (0.52, 0.05, 0.24),
                     (-0.25, 0.30, 0.28), (0.15, 0.48, 0.20))
            for dx, dy, br in blobs:
                bx, by = px(cx) + dx * rr, cyx + dy * rr
                draw.ellipse([bx - br * rr, by - br * rr * 0.7,
                              bx + br * rr, by + br * rr * 0.7],
                             fill=(86, 150, 92))
            draw.ellipse([px(cx) - rr, cyx - rr, px(cx) + rr, cyx + rr],
                         outline=(220, 235, 240), width=2)
        elif kind == "pylon":
            _, cx, fy, s, col = op
            top = py(fy - s)
            draw.line([px(cx - s * 0.4), py(fy), px(cx), top], fill=col, width=3)
            draw.line([px(cx + s * 0.4), py(fy), px(cx), top], fill=col, width=3)
            draw.line([px(cx - s * 0.28), py(fy - s * 0.35),
                       px(cx + s * 0.28), py(fy - s * 0.35)], fill=col, width=2)
            draw.line([px(cx - s * 0.17), py(fy - s * 0.65),
                       px(cx + s * 0.17), py(fy - s * 0.65)], fill=col, width=2)
        elif kind == "scales":
            _, cx, fy, s, col = op
            topy = py(fy - s)
            draw.line([px(cx), topy, px(cx), py(fy)], fill=col, width=3)
            draw.line([px(cx - s * 0.55), topy + 2, px(cx + s * 0.55),
                       topy + 2], fill=col, width=3)
            for side in (-0.55, 0.55):
                tx = px(cx + side * s)
                pan_y = topy + s * h * 0.42
                draw.line([tx, topy + 2, tx - 6, pan_y], fill=col, width=2)
                draw.line([tx, topy + 2, tx + 6, pan_y], fill=col, width=2)
                draw.arc([tx - 13, pan_y - 5, tx + 13, pan_y + 9],
                         start=0, end=180, fill=col, width=3)
            draw.line([px(cx - s * 0.3), py(fy), px(cx + s * 0.3), py(fy)],
                      fill=col, width=4)
        elif kind == "thermo":
            _, cx, fy, fw, level = op
            x = px(cx)
            tube_w = fw * w
            top = py(fy - 0.34)
            bot = py(fy + 0.30)
            draw.rounded_rectangle([x - tube_w / 2, top, x + tube_w / 2, bot],
                                   radius=tube_w / 2, outline=(235, 240, 242),
                                   width=3)
            fill_top = bot - (bot - top) * level
            draw.rectangle([x - tube_w * 0.22, fill_top, x + tube_w * 0.22,
                            bot], fill=(216, 60, 50))
            br = tube_w * 0.85
            draw.ellipse([x - br, bot - 2, x + br, bot - 2 + 2 * br],
                         fill=(216, 60, 50))
            for i in range(4):
                ty = top + (bot - top) * (i + 0.5) / 4
                draw.line([x + tube_w * 0.7, ty, x + tube_w * 1.15, ty],
                          fill=(235, 240, 242), width=2)
        elif kind == "spiral":
            _, cx, cy, r, col = op
            cxp, cyp = px(cx), py(cy)
            for i, rr in enumerate((0.30, 0.52, 0.74, 0.96)):
                rad = r * w * rr
                start = (i * 55) % 360
                draw.arc([cxp - rad, cyp - rad * 0.82, cxp + rad,
                          cyp + rad * 0.82], start=start, end=start + 265,
                         fill=col, width=4)
        elif kind == "bridge":
            _, fx, fy, fw, fh, col = op
            deck_y = py(fy)
            draw.line([px(fx), deck_y, px(fx + fw), deck_y], fill=col, width=4)
            for tx in (fx + fw * 0.28, fx + fw * 0.72):
                draw.line([px(tx), py(fy - fh), px(tx), py(fy + fh * 0.8)],
                          fill=col, width=4)
                for k in range(1, 5):
                    sx = fx + fw * (k / 5)
                    draw.line([px(tx), py(fy - fh), px(sx), deck_y],
                              fill=col, width=1)
            draw.arc([px(fx + fw * 0.28), deck_y - fh * h * 0.1,
                      px(fx + fw * 0.72), deck_y + fh * h * 1.15],
                     start=0, end=180, fill=col, width=3)
        elif kind == "missile":
            _, ax, ay, bx, by = op
            for i in range(1, 6):
                t = i / 6
                sx, sy = px(ax + (bx - ax) * t * 0.8), py(ay + (by - ay) * t * 0.8)
                if i % 2 == 0:
                    draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2],
                                 fill=(200, 200, 205))
            draw.line([px(ax + (bx - ax) * 0.8), py(ay + (by - ay) * 0.8),
                       px(bx), py(by)], fill=(225, 228, 232), width=8)
            draw.polygon([(px(ax + (bx - ax) * 0.8), py(ay + (by - ay) * 0.8)),
                          (px(ax + (bx - ax) * 0.72), py(ay + (by - ay) * 0.72) - 6),
                          (px(ax + (bx - ax) * 0.70), py(ay + (by - ay) * 0.70) + 5)],
                         fill=(255, 150, 60))
        elif kind == "stumps":
            _, cx, fy, s, col = op
            sw = s * w / 3.6
            for i in (-1, 0, 1):
                sx = px(cx) + i * sw * 1.25
                draw.rectangle([sx - sw / 2, py(fy - s), sx + sw / 2, py(fy)],
                               fill=col)
            draw.rectangle([px(cx) - sw * 1.6, py(fy - s) - 3,
                            px(cx) - sw * 0.2, py(fy - s)], fill=col)
            draw.rectangle([px(cx) + sw * 0.2, py(fy - s) - 3,
                            px(cx) + sw * 1.6, py(fy - s)], fill=col)
        else:
            raise ValueError("unknown paint op: %r" % (kind,))


# ------------------------------------------------------------------- data

REGION_COLOR = {
    "ASIA": (196, 44, 40),
    "EUROPE": (38, 84, 150),
    "AMERICAS": (30, 128, 84),
    "AFRICA": (222, 142, 26),
    "MIDDLE EAST": (128, 52, 140),
    "OCEANIA": (16, 128, 140),
    "WORLD": (96, 96, 100),
}

REGION_BAR = [("ASIA", 9), ("EUROPE", 9), ("AMERICAS", 8), ("AFRICA", 5),
              ("MIDDLE EAST", 4), ("OCEANIA", 3), ("WORLD", 2)]

NUMBERS = [
    ("$81.3BN", "Anthropic's record IPO raise"),
    ("9-6", "World Court genocide vote"),
    ("109-0", "Denmark's vote on the Arctic pact"),
    ("551,864", "sit Korea's entrance exam"),
    ("204,070", "listed to evacuate in Odisha"),
    ("4.9%", "Australian jobless, five-year high"),
    ("13 YRS", "between GTA V and GTA VI"),
]

STORIES = [
    dict(n=1, kicker="SHENZHEN · SUMMIT", region="ASIA",
         headline="Trump, Xi and Putin hold first three-way summit",
         deck="The three leaders met in Shenzhen and issued a four-point "
              "peace declaration on nuclear risk, UN reform and energy. "
              "Ukraine was not mentioned.",
         chip="4 POINTS", pin=(114.06, 22.55),
         scene=[("bg", (26, 36, 60)),
                ("flag", 0.05, 0.10, 0.15, 0.26, "us"),
                ("flag", 0.425, 0.08, 0.15, 0.28, "cn"),
                ("flag", 0.80, 0.10, 0.15, 0.26, "ru"),
                ("person", 0.235, 0.40, 0.42, (238, 214, 190), (28, 38, 80)),
                ("person", 0.50, 0.38, 0.44, (240, 206, 172), (128, 22, 24)),
                ("person", 0.765, 0.40, 0.42, (232, 210, 188), (38, 38, 44)),
                ("poly", [(0.06, 1.0), (0.15, 0.60), (0.85, 0.60),
                          (0.94, 1.0)], (94, 64, 38)),
                ("text", 0.235, 0.84, "TRUMP", 9, (255, 255, 255)),
                ("text", 0.50, 0.84, "XI", 9, (255, 255, 255)),
                ("text", 0.725, 0.84, "PUTIN", 9, (255, 255, 255))]),
    dict(n=2, kicker="THE HAGUE · JUSTICE", region="EUROPE",
         headline="World Court: Myanmar committed genocide",
         deck="By nine votes to six, the court found Myanmar guilty of "
              "genocide against the Rohingya and ordered reparations "
              "— a first for the court.",
         chip="9-6", pin=(4.32, 52.08),
         scene=[("bg", (198, 216, 230)),
                ("rect", 0.315, 0.20, 0.37, 0.52, (242, 240, 232)),
                ("poly", [(0.29, 0.20), (0.50, 0.03), (0.71, 0.20)],
                 (122, 62, 52)),
                ("rect", 0.465, 0.27, 0.07, 0.16, (255, 255, 255)),
                ("line", 0.50, 0.35, 0.50, 0.295, (60, 60, 60), 2),
                ("line", 0.50, 0.35, 0.53, 0.375, (60, 60, 60), 2),
                ("rect", 0.07, 0.32, 0.19, 0.40, (240, 238, 230)),
                ("poly", [(0.05, 0.32), (0.165, 0.22), (0.28, 0.32)],
                 (122, 62, 52)),
                ("rect", 0.74, 0.32, 0.19, 0.40, (240, 238, 230)),
                ("poly", [(0.72, 0.32), (0.835, 0.22), (0.95, 0.32)],
                 (122, 62, 52)),
                ("rect", 0.03, 0.72, 0.94, 0.05, (122, 62, 52)),
                ("scales", 0.50, 0.99, 0.30, (44, 44, 48))]),
    dict(n=3, kicker="NEW YORK · MARKETS", region="AMERICAS",
         headline="Anthropic starts trading in record IPO debut",
         deck="The Claude maker's shares opened at $111.50, a third above "
              "the $83 offer price, then slid under $100 as the debut "
              "rattled the wider AI trade.",
         chip="$111.50", pin=(-74.01, 40.71),
         scene=[("bg", (10, 34, 24)),
                ("text", 0.13, 0.05, "ANT", 19, (255, 255, 255)),
                ("dashed", 0.04, 0.32, 0.96, 0.32, (86, 130, 104)),
                ("dashed", 0.04, 0.62, 0.96, 0.62, (86, 130, 104)),
                ("polyline", [(0.05, 0.80), (0.24, 0.74), (0.38, 0.44),
                              (0.47, 0.15), (0.57, 0.30), (0.71, 0.52),
                              (0.95, 0.58)], (84, 230, 142), 3),
                ("circle", 0.47, 0.15, 0.016, (255, 130, 130)),
                ("bars", 0.60, 0.97, [0.26, 0.40, 0.33, 0.52, 0.42], 0.34,
                 (44, 110, 74))]),
    dict(n=4, kicker="ANTALYA · CLIMATE", region="EUROPE",
         headline="COP31 draft drops fossil fuels",
         deck="The slim draft drops fossil fuels and the $120bn aid goal.",
         chip="SLIM DRAFT", pin=(24.0, 40.0),
         scene=[("bg", (16, 52, 58)),
                ("thermo", 0.28, 0.52, 0.13, 0.72),
                ("rect", 0.56, 0.14, 0.36, 0.52, (245, 245, 240)),
                ("line", 0.60, 0.26, 0.88, 0.26, (150, 150, 150), 2),
                ("line", 0.60, 0.38, 0.88, 0.38, (150, 150, 150), 2),
                ("line", 0.60, 0.50, 0.82, 0.50, (150, 150, 150), 2),
                ("line", 0.565, 0.11, 0.915, 0.69, (200, 40, 40), 3),
                ("line", 0.915, 0.11, 0.565, 0.69, (200, 40, 40), 3),
                ("dots", 0.06, 0.10, 0.10, 0.20, 2, (140, 210, 190))]),
    dict(n=5, kicker="WORLDWIDE · GAMES", region="AMERICAS",
         headline="GTA VI goes on sale after 13 years",
         deck="Unlocked at midnight, NZ first; 15.9m pre-orders. "
              "PS5 and Xbox only.",
         chip="VI", pin=(-80.19, 25.76),
         scene=[("bg", (26, 14, 46)),
                ("rect", 0.0, 0.52, 1.0, 0.05, (255, 110, 140)),
                ("rect", 0.0, 0.615, 1.0, 0.03, (120, 240, 255)),
                ("building", 0.03, 0.28, 0.11, 0.50, (42, 26, 72)),
                ("building", 0.17, 0.18, 0.12, 0.60, (50, 30, 84)),
                ("building", 0.55, 0.22, 0.11, 0.56, (42, 26, 72)),
                ("building", 0.85, 0.28, 0.11, 0.50, (50, 30, 84)),
                ("dots", 0.045, 0.32, 0.09, 0.42, 3, (120, 240, 255)),
                ("dots", 0.185, 0.22, 0.10, 0.52, 3, (255, 140, 220)),
                ("dots", 0.565, 0.26, 0.09, 0.48, 3, (120, 240, 255)),
                ("rect", 0.0, 0.78, 1.0, 0.22, (14, 9, 28)),
                ("rrect", 0.31, 0.56, 0.38, 0.32, (18, 18, 26)),
                ("circle", 0.415, 0.72, 0.030, (235, 235, 235)),
                ("line", 0.345, 0.72, 0.378, 0.72, (235, 235, 235), 2),
                ("line", 0.361, 0.665, 0.361, 0.775, (235, 235, 235), 2),
                ("circle", 0.585, 0.685, 0.020, (255, 90, 120)),
                ("circle", 0.618, 0.74, 0.020, (90, 200, 255))]),
    dict(n=6, kicker="ODISHA · STORM", region="ASIA",
         headline="Cyclone Akvan nears India's coast",
         deck="204,070 listed for evacuation; landfall due Friday "
              "near Puri.",
         chip="LANDFALL FRI", pin=(85.83, 19.80),
         scene=[("bg", (70, 84, 98)),
                ("spiral", 0.36, 0.42, 0.19, (235, 240, 245)),
                ("line", 0.08, 0.08, 0.03, 0.30, (200, 215, 230), 2),
                ("line", 0.20, 0.05, 0.15, 0.27, (200, 215, 230), 2),
                ("line", 0.90, 0.06, 0.85, 0.28, (200, 215, 230), 2),
                ("poly", [(0.0, 0.86), (0.25, 0.78), (0.55, 0.84),
                          (0.8, 0.79), (1.0, 0.85), (1.0, 1.0), (0.0, 1.0)],
                 (196, 178, 140)),
                ("pylon", 0.86, 0.82, 0.30, (40, 40, 44))]),
    dict(n=7, kicker="CRIMEA · WAR", region="EUROPE",
         headline="Ukraine hits Crimea bridge again",
         deck="Third strike in a week; the rail section was hit, "
              "traffic halted.",
         chip="3RD STRIKE", pin=(36.50, 45.30),
         scene=[("bg", (14, 20, 38)),
                ("rect", 0.0, 0.82, 1.0, 0.18, (10, 16, 30)),
                ("bridge", 0.03, 0.62, 0.94, 0.34, (150, 160, 180)),
                ("dots", 0.42, 0.36, 0.16, 0.20, 3, (255, 150, 60)),
                ("circle", 0.52, 0.30, 0.035, (120, 120, 125)),
                ("circle", 0.585, 0.22, 0.05, (105, 105, 112)),
                ("circle", 0.465, 0.24, 0.026, (132, 132, 138)),
                ("circle", 0.88, 0.13, 0.028, (228, 228, 208))]),
    dict(n=8, kicker="RIYADH · WAR", region="MIDDLE EAST",
         headline="Saudis shoot down Houthi missile",
         deck="Sirens at 04:42; debris caused damage, no casualties "
              "reported.",
         chip="04:42", pin=(48.0, 23.0),
         scene=[("bg", (38, 30, 52)),
                ("buildings", 0.02, 0.30, 0.96, 0.48, (16, 14, 26)),
                ("rect", 0.0, 0.78, 1.0, 0.22, (20, 16, 30)),
                ("missile", 0.14, 0.70, 0.52, 0.16),
                ("dots", 0.56, 0.06, 0.15, 0.18, 3, (255, 210, 120)),
                ("circle", 0.90, 0.12, 0.026, (240, 240, 230))]),
    dict(n=9, kicker="GAZA · CEASEFIRE", region="MIDDLE EAST",
         headline="Israel says Gaza tank raid is over",
         deck="The army told AFP the push past the Yellow Line "
              "is complete.",
         chip="RAID OVER", pin=(36.5, 30.0),
         scene=[("bg", (104, 92, 66)),
                ("rect", 0.0, 0.76, 1.0, 0.24, (88, 76, 54)),
                ("tank", 0.21, 0.84, 0.34, (52, 54, 44)),
                ("dashed", 0.52, 0.06, 0.52, 0.72, (240, 220, 90)),
                ("rect", 0.52, 0.05, 0.075, 0.055, (240, 220, 90)),
                ("poly", [(0.60, 0.82), (0.68, 0.60), (0.76, 0.82)],
                 (226, 218, 196)),
                ("poly", [(0.735, 0.84), (0.80, 0.66), (0.865, 0.84)],
                 (216, 206, 182)),
                ("poly", [(0.85, 0.85), (0.905, 0.71), (0.96, 0.85)],
                 (226, 218, 196))]),
    dict(n=10, kicker="BOGOTÁ · LABOUR", region="AMERICAS",
         headline="Colombia's unions strike nationwide",
         deck="Marches in Bogotá, Medellín and Cali against the "
              "rescue bill.",
         chip="3 CITIES", pin=(-74.08, 4.71),
         scene=[("bg", (168, 198, 220)),
                ("buildings", 0.02, 0.26, 0.96, 0.36, (120, 140, 165)),
                ("rrect", 0.16, 0.22, 0.68, 0.21, (248, 248, 246)),
                ("text", 0.50, 0.265, "PARO NACIONAL", 10, (178, 30, 40)),
                ("crowd", 0.04, 0.985, 0.92, 0.32, (60, 60, 70))]),
    dict(n=11, kicker="CANBERRA · ECONOMY", region="OCEANIA",
         headline="Australia's jobless rate hits 4.9%",
         deck="A five-year high. 43,500 jobs lost; a gain of 25,000 "
              "was forecast.",
         chip="4.9%", pin=(149.13, -35.28),
         scene=[("bg", (240, 242, 238)),
                ("bar", 0.10, 0.90, 0.11, 0.28, (52, 90, 140)),
                ("bar", 0.26, 0.90, 0.11, 0.36, (52, 90, 140)),
                ("bar", 0.42, 0.90, 0.11, 0.44, (52, 90, 140)),
                ("bar", 0.58, 0.90, 0.11, 0.40, (52, 90, 140)),
                ("bar", 0.74, 0.90, 0.11, 0.60, (190, 44, 40)),
                ("line", 0.05, 0.90, 0.97, 0.90, (120, 120, 120), 2),
                ("arrow", 0.66, 0.14, 0.86, 0.26, (190, 44, 40))]),
    dict(n=12, kicker="JAKARTA · LAW", region="ASIA",
         headline="Indonesia passes asset-seizure law",
         deck="Seizure of suspect assets of Rp1bn or more, without "
              "a conviction.",
         chip="18-YEAR WAIT", pin=(106.85, -6.21),
         scene=[("bg", (210, 200, 180)),
                ("poly", [(0.14, 0.28), (0.50, 0.05), (0.86, 0.28)],
                 (150, 130, 100)),
                ("rect", 0.14, 0.28, 0.72, 0.06, (150, 130, 100)),
                ("rect", 0.20, 0.36, 0.06, 0.40, (238, 232, 216)),
                ("rect", 0.385, 0.36, 0.06, 0.40, (238, 232, 216)),
                ("rect", 0.57, 0.36, 0.06, 0.40, (238, 232, 216)),
                ("rect", 0.755, 0.36, 0.06, 0.40, (238, 232, 216)),
                ("rect", 0.12, 0.76, 0.76, 0.06, (150, 130, 100)),
                ("rrect", 0.445, 0.42, 0.11, 0.26, (178, 30, 40)),
                ("dots", 0.462, 0.465, 0.075, 0.17, 2, (255, 255, 255))]),
    dict(n=13, kicker="WELLINGTON · SPORT", region="OCEANIA",
         headline="Nicholls, Phillips rescue New Zealand",
         deck="From 70 for 5, an unbroken 173-run stand took NZ "
              "to 243 for 5.",
         chip="243/5", pin=(174.78, -41.29),
         scene=[("bg", (40, 96, 48)),
                ("rect", 0.0, 0.0, 1.0, 0.09, (30, 70, 38)),
                ("dots", 0.02, 0.012, 0.96, 0.065, 2, (220, 230, 220)),
                ("rect", 0.44, 0.05, 0.12, 0.90, (206, 186, 140)),
                ("rect", 0.478, 0.10, 0.008, 0.07, (250, 200, 60)),
                ("rect", 0.493, 0.10, 0.008, 0.07, (250, 200, 60)),
                ("rect", 0.508, 0.10, 0.008, 0.07, (250, 200, 60)),
                ("rect", 0.478, 0.83, 0.008, 0.07, (250, 200, 60)),
                ("rect", 0.493, 0.83, 0.008, 0.07, (250, 200, 60)),
                ("rect", 0.508, 0.83, 0.008, 0.07, (250, 200, 60)),
                ("rect", 0.618, 0.485, 0.024, 0.07, (200, 40, 40))]),
]

ALSO = [
    ("Seoul: 551,864 sit the Suneung entrance exam", "ASIA"),
    ("Seoul: top court orders ex-PM Han's retrial", "ASIA"),
    ("Shenzhen: APEC leaders adopt a joint declaration", "ASIA"),
    ("Shenzhen: Xi urges a ban on all nuclear arms", "ASIA"),
    ("Albanese to Putin: 'End your war, end it now'", "ASIA"),
    ("Doha: Rising Stars Asia Cup opens, eight teams", "ASIA"),
    ("Copenhagen: Arctic pact approved 109-0", "EUROPE"),
    ("Brussels: EU delays methane rules two years", "EUROPE"),
    ("London: Bayesian yacht was vulnerable to wind", "EUROPE"),
    ("Kyiv says it hit two Krasnodar oil refineries", "EUROPE"),
    ("Ukraine left off the Shenzhen summit agenda", "EUROPE"),
    ("Paris: Mélenchon could win, minister concedes", "EUROPE"),
    ("Washington: Liu Yunping chairs House caucus", "AMERICAS"),
    ("Washington: Democrats order records preserved", "AMERICAS"),
    ("Washington: senators warn on AI cyber threats", "AMERICAS"),
    ("Florida floods shut Broward, Miami schools", "AMERICAS"),
    ("Bolivia declares an El Niño emergency", "AMERICAS"),
    ("Hormuz: Iran says mines set five tankers ablaze", "MIDDLE EAST"),
    ("Jazan: Saudi all-clear in three southern cities", "MIDDLE EAST"),
    ("Sudan court sentences absent RSF chief to death", "AFRICA"),
    ("Mogadishu: Somalia expels the UAE ambassador", "AFRICA"),
    ("Libya: cocaine, millions of pills seized in east", "AFRICA"),
    ("Canaries: 11,000 migrants arrive in 15 days", "AFRICA"),
    ("Nairobi: Jepchirchir banned three years, doping", "AFRICA"),
    ("Tonga: drought emergency takes effect", "OCEANIA"),
    ("Space: a red giant is seen eating a Sun-sized star", "WORLD"),
    ("Zurich: two rivals to challenge FIFA's Infantino", "WORLD"),
]

DATE_CHECK = (
    "DATE CHECK — Not in this edition: stories first reported on "
    "18 November or earlier: Voyager 1 crossing one light-day "
    "(10:16 GMT Wednesday) · Nvidia's $115.8bn quarter · Anthropic's "
    "$83 share pricing · the EU's €45bn Ukraine loan · the FOMC minutes "
    "and the Dow's 561-point fall · Van Gogh's record $190.4m sale · "
    "Carney on China ties."
)

FOOTER_1 = ("Every story on this page happened, or was first reported, "
            "on Thursday 19 November 2026. Disputed claims are "
            "attributed, not stated as fact.")
FOOTER_2 = ("Pictures and map: original, drawn in code. Sources: Reuters, "
            "AP, AFP, BBC, Al Jazeera, Xinhua, Euronews, ABC, RNZ, Kompas, "
            "ESPNcricinfo. — The Global Ledger")


# ------------------------------------------------------------- rendering

def masthead(draw):
    kf = font(SANS_B, 14)
    tracked_text(draw, MARGIN, 14, "THE WORLD IN ONE DAY", kf, ACCENT, 3)
    rf = font(SANS, 11)
    right = "40 STORIES · EVERY CONTINENT · ALL FROM THIS ONE DAY"
    rw = tracked_width(draw, right, rf, 2)
    tracked_text(draw, W - MARGIN - rw, 16, right, rf, MUTE, 2)
    draw.text((MARGIN, 32), "Thursday 19 November 2026",
              font=font(SERIF_B, 55), fill=INK)
    draw.text((MARGIN, 96),
              "Trump, Xi and Putin share one table · The World Court "
              "finds genocide in Myanmar · COP31's draft drops fossil fuels",
              font=font(SERIF_I, 16), fill=(150, 30, 36))
    draw.rectangle([MARGIN, 120, W - MARGIN, 122], fill=RULE)
    draw.rectangle([MARGIN, 125, W - MARGIN, 126], fill=RULE)


def region_bar(draw):
    y, hh = 132, 25
    total = sum(c for _, c in REGION_BAR)
    x = MARGIN
    lf = font(SANS_B, 9.5)
    sf = font(SANS_B, 9)
    for name, count in REGION_BAR:
        wseg = PAGE_W * count / total
        col = REGION_COLOR[name]
        draw.rectangle([x, y, x + wseg - 2, y + hh], fill=col)
        label = "%s %d" % (name, count)
        lw = draw.textlength(label, font=lf)
        if lw <= wseg - 6:
            draw.text((x + (wseg - 2 - lw) / 2, y + 7.5), label, font=lf,
                      fill=(255, 255, 255))
        else:
            draw.text((x + 1, y + hh + 3), label, font=sf, fill=col)
        x += wseg


def numbers_strip(draw):
    tf = font(SANS_B, 12)
    tracked_text(draw, MARGIN, 174, "THE DAY IN NUMBERS", tf, ACCENT, 2)
    colw = PAGE_W / len(NUMBERS)
    bf = font(SERIF_B, 21)
    cf = font(SANS, 9)
    for i, (big, cap) in enumerate(NUMBERS):
        x = MARGIN + i * colw
        draw.text((x, 192), big, font=bf, fill=INK)
        for j, ln in enumerate(wrap(draw, cap, cf, colw - 10)[:2]):
            draw.text((x, 218 + j * 11), ln, font=cf, fill=MUTE)
    draw.rectangle([MARGIN, 242, W - MARGIN, 243], fill=RULE)


def story_cell(draw, st, x, y, w, scene_h, hl_size, hl_lh, deck_size,
               deck_lh, small):
    paint(draw, (x, y, w, scene_h), st["scene"])
    draw.rectangle([x, y, x + w, y + scene_h], outline=RULE, width=1)
    cf = font(SANS_B, 10)
    chip = st["chip"]
    cw = draw.textlength(chip, font=cf) + 12
    cx = x + w - cw - 5
    cy = y + scene_h - 22
    draw.rectangle([cx, cy, cx + cw, cy + 17], fill=CHIP_BG)
    draw.text((cx + 6, cy + 3), chip, font=cf, fill=(255, 255, 255))
    ty = y + scene_h + 5
    bs = 15 if small else 17
    draw.rectangle([x, ty, x + bs, ty + bs], fill=ACCENT)
    nf = font(SANS_B, 10 if small else 11)
    num = str(st["n"])
    nw = draw.textlength(num, font=nf)
    draw.text((x + (bs - nw) / 2, ty + 2.5), num, font=nf,
              fill=(255, 255, 255))
    rg = st["region"]
    rf = font(SANS_B, 8.5 if small else 9)
    rw2 = draw.textlength(rg, font=rf) + 10
    rx = x + bs + 5
    draw.rectangle([rx, ty, rx + rw2, ty + bs], fill=REGION_COLOR[rg])
    draw.text((rx + 5, ty + (3.5 if small else 4)), rg, font=rf,
              fill=(255, 255, 255))
    kf = font(SANS_B, 9 if small else 10)
    tracked_text(draw, rx + rw2 + 6, ty + (3.5 if small else 4),
                 st["kicker"], kf, MUTE, 0 if small else 1)
    ty += bs + 4
    hf = font(SERIF_B, hl_size)
    for ln in wrap(draw, st["headline"], hf, w):
        draw.text((x, ty), ln, font=hf, fill=INK)
        ty += hl_lh
    ty += 1
    df = font(SERIF, deck_size)
    for ln in wrap(draw, st["deck"], df, w):
        draw.text((x, ty), ln, font=df, fill=(52, 48, 42))
        ty += deck_lh
    return ty


MAP_POLYS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-80, 73), (-75, 62), (-65, 60), (-55, 52), (-60, 46), (-70, 44),
     (-74, 40), (-76, 35), (-80, 32), (-80, 26), (-84, 30), (-90, 21),
     (-97, 16), (-105, 20), (-110, 24), (-114, 29), (-117, 33), (-122, 37),
     (-124, 46), (-132, 56), (-152, 60), (-165, 60)],
    [(-45, 60), (-30, 68), (-22, 70), (-20, 76), (-30, 82), (-50, 80),
     (-58, 76), (-55, 70), (-52, 64)],
    [(-79, 9), (-72, 12), (-64, 10), (-55, 6), (-50, 0), (-44, -3),
     (-35, -8), (-39, -13), (-40, -20), (-48, -26), (-52, -32), (-57, -38),
     (-62, -41), (-65, -45), (-67, -50), (-68, -54), (-71, -54), (-73, -46),
     (-73, -37), (-71, -30), (-70, -20), (-75, -15), (-79, -8), (-80, -4),
     (-77, 1), (-78, 4)],
    [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31),
     (35, 28), (38, 22), (40, 15), (43, 12), (48, 11), (51, 12), (46, 5),
     (42, -2), (40, -10), (38, -18), (36, -22), (33, -27), (28, -33),
     (20, -35), (17, -32), (15, -27), (13, -18), (12, -10), (13, -2),
     (9, 4), (8, 5), (-8, 5), (-13, 8), (-17, 15), (-17, 20), (-16, 24),
     (-13, 28), (-9, 31)],
    [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-5, 48), (0, 50), (5, 53),
     (8, 54), (8, 57), (5, 58), (5, 60), (10, 59), (18, 60), (21, 60),
     (25, 60), (28, 60), (30, 55), (28, 50), (30, 46), (26, 44), (28, 41),
     (24, 40), (23, 36), (19, 40), (15, 42), (18, 45), (13, 45), (12, 42),
     (16, 38), (12, 38), (8, 44), (3, 43), (0, 39), (-2, 37)],
    [(26, 41), (30, 46), (28, 50), (30, 55), (28, 60), (30, 65), (40, 66),
     (50, 68), (65, 69), (80, 72), (95, 76), (110, 74), (125, 72),
     (140, 72), (155, 71), (170, 67), (178, 65), (170, 60), (160, 58),
     (156, 52), (150, 45), (142, 48), (140, 40), (138, 36), (132, 33),
     (128, 30), (124, 28), (121, 24), (116, 23), (110, 20), (108, 14),
     (106, 9), (103, 6), (100, 7), (98, 11), (96, 15), (93, 17), (90, 22),
     (87, 21), (83, 18), (80, 13), (77, 8), (75, 13), (72, 19), (68, 23),
     (66, 25), (61, 25), (57, 26), (54, 26), (51, 29), (49, 30), (50, 27),
     (54, 24), (57, 23), (59, 22), (56, 19), (53, 16), (48, 14), (45, 12),
     (43, 12), (41, 15), (39, 20), (36, 28), (34, 31), (36, 36), (33, 36),
     (30, 36), (27, 37)],
    [(95, 5), (101, 3), (107, 2), (112, 1), (117, 0), (122, -1), (128, -3),
     (133, -3), (138, -2), (142, -2), (147, -3), (150, -8), (145, -7),
     (140, -8), (135, -9), (130, -8), (125, -8), (120, -7), (115, -6),
     (110, -5), (105, -3), (100, 0)],
    [(109, 1), (113, 4), (117, 6), (119, 2), (118, -2), (115, -3),
     (111, -2)],
    [(130, 31), (133, 34), (137, 35), (140, 36), (141, 40), (142, 44),
     (144, 44), (142, 42), (140, 38), (138, 36), (135, 34), (132, 33)],
    [(-5, 50), (-3, 53), (-5, 55), (-3, 57), (-2, 58), (-1, 57), (0, 54),
     (1, 52), (0, 51)],
    [(113, -22), (114, -28), (115, -34), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (137, -35), (139, -37), (141, -38), (145, -38),
     (147, -38), (150, -37), (153, -32), (153, -27), (151, -24), (149, -20),
     (146, -19), (143, -15), (142, -11), (142, -14), (140, -18), (139, -20),
     (136, -15), (135, -12), (132, -11), (130, -13), (126, -14), (122, -17),
     (118, -20)],
    [(167, -45), (169, -43), (171, -42), (173, -39), (175, -37), (177, -38),
     (176, -40), (174, -41), (172, -43), (169, -46)],
]


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(233, 228, 214))

    def proj(lon, lat):
        return (x + (lon + 170) / 360 * w, y + (84 - lat) / 142 * h)

    for pts in MAP_POLYS:
        draw.polygon([proj(a, b) for a, b in pts], fill=(198, 188, 162))
    nf = font(SANS_B, 8)
    for st in STORIES:
        cx, cy = proj(*st["pin"])
        col = REGION_COLOR[st["region"]]
        r = 6.5
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col,
                     outline=(255, 255, 255), width=1)
        num = str(st["n"])
        nw = draw.textlength(num, font=nf)
        draw.text((cx - nw / 2, cy - 4.5), num, font=nf,
                  fill=(255, 255, 255))
    draw.text((x + 8, y + h - 16), "Numbers match the stories above.",
              font=font(SERIF_I, 10), fill=MUTE)


def also_section(draw, x, y, w):
    hf = font(SANS_B, 12)
    tracked_text(draw, x, y, "ALSO ON THURSDAY 19 NOVEMBER", hf, ACCENT, 2)
    col_w = (w - 16) / 2
    items = list(enumerate(ALSO, start=14))
    half = (len(items) + 1) // 2
    nf = font(SANS_B, 10)
    tf = font(SANS, 10)
    for ci, col_items in enumerate((items[:half], items[half:])):
        cx = x + ci * (col_w + 16)
        cy = y + 20
        for num, (text, region) in col_items:
            nstr = "%d " % num
            draw.text((cx, cy), nstr, font=nf, fill=REGION_COLOR[region])
            nw = draw.textlength(nstr, font=nf)
            lines = wrap(draw, text, tf, col_w - nw)
            for j, ln in enumerate(lines):
                draw.text((cx + nw, cy + j * 12), ln, font=tf, fill=INK)
            cy += len(lines) * 12 + 1.2


def bottom_boxes(draw):
    y = 948
    df = font(SANS, 10)
    lines = wrap(draw, DATE_CHECK, df, PAGE_W - 20)
    hh = len(lines) * 12 + 9
    draw.rectangle([MARGIN, y, W - MARGIN, y + hh], outline=ACCENT, width=1)
    for i, ln in enumerate(lines):
        draw.text((MARGIN + 10, y + 5 + i * 12), ln, font=df,
                  fill=(120, 26, 32))
    fy = y + hh + 6
    ff = font(SANS, 9.5)
    draw.text((MARGIN, fy), FOOTER_1, font=ff, fill=MUTE)
    draw.text((MARGIN, fy + 12), FOOTER_2, font=ff, fill=MUTE)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    masthead(draw)
    region_bar(draw)
    numbers_strip(draw)
    lw = (PAGE_W - 20) / 3
    for i, st in enumerate(STORIES[:3]):
        story_cell(draw, st, MARGIN + i * (lw + 10), 248, lw, 80, 24, 26,
                   12.5, 14.5, small=False)
    gw = (PAGE_W - 32) / 5
    for r in range(2):
        for c in range(5):
            st = STORIES[3 + r * 5 + c]
            story_cell(draw, st, MARGIN + c * (gw + 8), 452 + r * 146, gw,
                       58, 17, 19, 10.5, 12, small=True)
    hf = font(SANS_B, 12)
    tracked_text(draw, MARGIN, 744, "WHERE IT HAPPENED", hf, ACCENT, 2)
    draw_map(draw, MARGIN, 764, 330, 178)
    also_section(draw, 368, 744, W - MARGIN - 368)
    bottom_boxes(draw)
    img.save("entry.png")
    print("wrote entry.png")


if __name__ == "__main__":
    main()
