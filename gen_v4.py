#!/usr/bin/env python3
# The Global Ledger — Thursday 19 November 2026 (news-image-20261119, v4).
# Hans's v4 brief: keep v3's generated scenes, restore v2's text depth —
# full prose decks that are NEVER truncated, and complete ALSO briefs
# (headline + fact + source, whole statements, no mid-sentence cuts).
# 36 stories: 3 leads + 10 grid (all illustrated) + 23 ALSO briefs.
# Every story happened or was first reported on Thursday 19 Nov 2026.
# Renders entry.png at 1024x1024 and prints the measurement gate:
# unique colours and file bytes (submit gate: >= 18000 colours, >= 350 KB),
# plus a layout report asserting nothing overflows the page.
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
SCENES = os.path.join(BASE, "scenes")
W = H = 1024
PAPER = (243, 238, 226)
INK = (26, 24, 20)
RED = (154, 32, 24)
FAINT = (108, 100, 88)
IMG = Image.new("RGB", (W, H), PAPER)
D = ImageDraw.Draw(IMG)

FD = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)
SERIF = "DejaVuSerif-Bold.ttf"
SERIF_R = "DejaVuSerif.ttf"
SANS = "DejaVuSans-Bold.ttf"
SANS_R = "DejaVuSans.ttf"

def text(x, y, s, font, fill=INK, anchor="la"):
    D.text((x, y), s, font=font, fill=fill, anchor=anchor)

def rule(y, x0=28, x1=996, wdt=2, fill=INK):
    D.line([(x0, y), (x1, y)], fill=fill, width=wdt)

def wrap(s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if D.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines

# ---------------- story data ----------------
# bar = region-bar bucket; decks are complete: the layout below sizes every
# cell from the wrapped line count, so no deck is ever sliced.
STORIES = [
 dict(n=1, img="s01", pin=(655, 300), region="SHENZHEN · CHINA", bar="ASIA", color=(23, 58, 94),
      head="Three flags, one table: peace terms drafted in Shenzhen",
      deck="Trump, Xi and Putin close 90 minutes of talks with a four-point Declaration toward Peace — UN reform, more refined-fuel supply, immunity for state officials and a pledge that nuclear war must never be fought. Kyiv is not mentioned. — Xinhua; Kremlin readout; USA Today"),
 dict(n=2, img="s02", pin=(500, 268), region="THE HAGUE", bar="EUROPE", color=(38, 84, 124),
      head="World court: Myanmar committed genocide — a first in its history",
      deck="Judges rule 9–6 that Myanmar's army committed genocide against the Rohingya — the first state ever held responsible by the ICJ. Some 10,000 were killed and 730,000 driven into Bangladesh; reparations are ordered. — Court summary; wires"),
 dict(n=3, img="s03", pin=(215, 318), region="NEW YORK", bar="AMERICAS", color=(20, 92, 60),
      head="Anthropic's record debut: up a third at the open, +17% at the close",
      deck="The AI lab opens at $111.50, a third above its $83 offer price, peaks at $114.99 and closes at $97.17 — still +17% on debut. The $81.3bn raise is the largest IPO on record; 980 million shares change hands. — Exchange data; wires"),
 dict(n=4, img="s04", pin=(520, 292), region="ANTALYA", bar="EUROPE", tag="DRAFT",
      head="Fossil fuels struck out of the climate text",
      deck="Thursday's slimmed draft — nine pages, down from 18 — drops every fossil-fuel reference and the $120bn adaptation-aid target. — Draft text; wires"),
 dict(n=5, img="s05", pin=(228, 322), region="LOS SANTOS · GTA VI", bar="AMERICAS", tag="",
      head="Midnight in Los Santos: the wait ends tonight",
      deck="GTA VI unlocks at midnight after 15.9m pre-orders; midnight queues form outside game stores on three continents. — Retail trackers; wires"),
 dict(n=6, img="s06", pin=(688, 330), region="ODISHA", bar="ASIA", tag="FORECAST",
      head="Cyclone Akvan bears down on the Odisha coast",
      deck="More than 200,000 people are listed for evacuation as Akvan nears Puri; landfall is expected Friday. — IMD bulletin; state disaster office"),
 dict(n=7, img="s07", pin=(545, 262), region="KERCH BRIDGE", bar="EUROPE", tag="",
      head="Kerch Bridge hit for the third time in a week",
      deck="An overnight strike damages the rail section of the Crimean crossing; road and rail traffic is halted again. — Regional officials; wires"),
 dict(n=8, img="s08", pin=(590, 330), region="RIYADH", bar="MIDDLE EAST", tag="CLAIM",
      head="Missile downed over Riyadh before dawn",
      deck="A Houthi ballistic missile is intercepted over the capital at 04:42; sirens sound, and no casualties are reported. — Saudi defence ministry; wires"),
 dict(n=9, img="s09", pin=(560, 322), region="GAZA", bar="MIDDLE EAST", tag="",
      head="'It is over': Israel ends its Gaza ground operation",
      deck="Israel says the raid that began on Wednesday is complete and its forces are back behind the Yellow Line. — IDF statement; wires"),
 dict(n=10, img="s10", pin=(262, 385), region="BOGOTÁ · COLOMBIA", bar="AMERICAS", tag="",
      head="Colombia stops for a national strike",
      deck="Unions halt transport and schools in the first general strike of the Petro era; marches fill the capital. — Union federations; wires"),
 dict(n=11, img="s11", pin=(838, 468), region="CANBERRA", bar="OCEANIA", tag="",
      head="Australia's jobless rate jumps to 4.9%",
      deck="The economy sheds 43,500 jobs in October, the worst monthly loss in four years; the dollar slides. — ABS release; market data"),
 dict(n=12, img="s12", pin=(742, 392), region="JAKARTA", bar="ASIA", tag="",
      head="Jakarta can now seize assets without a conviction",
      deck="Parliament passes an asset-seizure law covering unexplained wealth above Rp1bn, even where no crime is proven. — DPR record; wires"),
 dict(n=13, img="s13", pin=(872, 512), region="WELLINGTON · CRICKET", bar="OCEANIA", tag="",
      head="Nicholls and Phillips rescue New Zealand at the Basin",
      deck="From 70 for 5, Nicholls (113*) and Phillips (94*) add an unbroken 173 to reach 243 for 5 at stumps; Bumrah takes 3–52. — Scorecard, NZ v IND, day 1"),
]

# Complete one-line briefs in v2's manner: headline + the key fact + source,
# written to fit the column whole — nothing is cut at render time.
ALSO = [
 ("ASIA", "551,864 sit Korea's Suneung exam at 1,310 centres; flights grounded for listening — Education ministry"),
 ("ASIA", "Seoul's council votes 61–29 to dissolve itself and force fresh elections — Yonhap"),
 ("ASIA", "Shenzhen opens a one-stop bureau for its 9,000 foreign-invested firms — Xinhua"),
 ("ASIA", "Tolls end on Shenzhen's Meiguan expressway, free after 31 years — Xinhua"),
 ("ASIA", "Seoul's top court orders a retrial for ex-PM Han — AP"),
 ("ASIA", "Albanese flies home from Shenzhen as summit season ends — AAP"),
 ("EUROPE", "Denmark ratifies the US–Greenland Arctic pact, 109–0 in the Folketing — Ritzau"),
 ("EUROPE", "Brussels opens a formal probe into X's recommender and ad library — Commission"),
 ("EUROPE", "Kyiv names an interim energy minister as winter blackouts loom — Presidential office"),
 ("EUROPE", "Paris metro workers give notice of a December strike over pay — Union notice"),
 ("EUROPE", "London's rent cap clears the Commons 312–268 and heads to the Lords — Hansard"),
 ("EUROPE", "Kyiv says it struck two Krasnodar oil refineries overnight — Euronews"),
 ("AMERICAS", "Washington tightens AI chip export licences for 12 states — Federal Register"),
 ("AMERICAS", "Florida counts the flood cost: insured losses top $900m — State regulator"),
 ("AFRICA", "Sudan's rivals agree a 72-hour truce, brokered in Jeddah — Mediators' statement"),
 ("AFRICA", "Somalia expels the UAE ambassador, giving him 48 hours — Foreign ministry"),
 ("AFRICA", "Canaries migrant arrivals pass 40,000 for the year, a record — Interior ministry"),
 ("AFRICA", "Nairobi's single ticket now covers buses, matatus and rail — City hall"),
 ("AFRICA", "Marathon champion Jepchirchir banned three years for doping — ABC"),
 ("MIDDLE EAST", "Hormuz tanker was boarded, then freed; crew safe, agencies confirm — UKMTO"),
 ("OCEANIA", "Tonga counts Cyclone Loto's damage; power cut across Tongatapu — NEMO office"),
 ("WORLD", "Voyager's first full light-day of data reaches JPL — JPL status"),
 ("WORLD", "Zurich votes 58–42 to keep its trams free after the trial — City result"),
]

BAR_ORDER = ["ASIA", "EUROPE", "AMERICAS", "AFRICA", "MIDDLE EAST", "OCEANIA", "WORLD"]
REGION_BAR = []
for b in BAR_ORDER:
    c = sum(1 for s in STORIES if s["bar"] == b) + sum(1 for r, _ in ALSO if r == b)
    if c:
        REGION_BAR.append((b, c))
TOTAL = sum(c for _, c in REGION_BAR)
assert TOTAL == 36, TOTAL

NUMBERS = [("9–6", "ICJ verdict: genocide"), ("$81.3bn", "Anthropic's record raise"),
           ("90 min", "inside the Shenzhen room"), ("4.9%", "Australia jobless"),
           ("204,070", "listed to evacuate, Odisha"), ("173*", "the Basin rescue stand"),
           ("109–0", "Folketing ratifies the pact")]

# ---------------- scene pasting ----------------
def paste_scene(box, name):
    x, y, w, h = box
    src = Image.open(os.path.join(SCENES, name + ".webp")).convert("RGB")
    sw, sh = src.size
    target = w / h
    if sw / sh > target:
        cw = int(sh * target)
        left, top, ch = (sw - cw) // 2, 0, sh
    else:
        cw = sw
        ch = int(sw / target)
        left, top = 0, int((sh - ch) * 0.46)
    src = src.crop((left, top, left + cw, top + ch)).resize((w, h), Image.LANCZOS)
    IMG.paste(src, (x, y))
    D.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)

def story_cell(st, x, y, w, scene_h, head_size, deck_size):
    """Render one illustrated story with its FULL deck; return bottom y."""
    paste_scene((x, y, w, scene_h), st["img"])
    nf = F(SANS, 12)
    label = f'{st["n"]} · {st["region"]}'
    tw = D.textlength(label, font=nf)
    D.rectangle([x + 5, y + 5, x + 11 + tw, y + 23], fill=INK)
    D.text((x + 8, y + 8), label, font=nf, fill=(250, 248, 240))
    if st.get("tag"):
        tf = F(SANS, 10)
        tag = st["tag"]
        tw2 = D.textlength(tag, font=tf)
        D.rectangle([x + w - 11 - tw2, y + 5, x + w - 5, y + 21], fill=RED)
        D.text((x + w - 8 - tw2, y + 8), tag, font=tf, fill=(250, 248, 240))
    cy = y + scene_h + 5
    hf = F(SERIF, head_size)
    for ln in wrap(st["head"], hf, w):
        D.text((x, cy), ln, font=hf, fill=INK)
        cy += head_size + 3
    df = F(SERIF_R, deck_size)
    for ln in wrap(st["deck"], df, w):
        D.text((x, cy), ln, font=df, fill=(52, 48, 42))
        cy += deck_size + 2
    return cy

# ---------------- masthead ----------------
text(512, 10, "THE GLOBAL LEDGER", F(SERIF, 54), anchor="ma")
text(512, 66, "THURSDAY 19 NOVEMBER 2026  ·  THE DAY IN ONE PAGE  ·  36 STORIES · EVERY CONTINENT · ALL FROM THIS ONE DAY",
     F(SANS, 11), fill=RED, anchor="ma")
rule(84, wdt=3)
rule(89, wdt=1)

# ---------------- the day in numbers ----------------
text(28, 94, "THE DAY IN NUMBERS", F(SANS, 12), fill=RED)
nx = 28
for val, cap in NUMBERS:
    vf = F(SERIF, 21)
    vw = D.textlength(val, font=vf)
    cf = F(SANS_R, 8)
    cw = max([D.textlength(l, font=cf) for l in wrap(cap, cf, 108)] + [0])
    cellw = int(max(vw, cw)) + 14
    D.text((nx, 110), val, font=vf, fill=INK)
    cyy = 136
    for ln in wrap(cap, cf, 108):
        D.text((nx, cyy), ln, font=cf, fill=FAINT)
        cyy += 10
    nx += cellw + 8
    if nx < 990:
        D.line([(nx - 8, 112), (nx - 8, 148)], fill=FAINT, width=1)
rule(156, wdt=1)

# ---------------- region bar (counts computed from the data) ----------------
ry = 160
D.rectangle([28, ry, 996, ry + 20], fill=INK)
rx = 40
for name, cnt in REGION_BAR:
    f = F(SANS, 11)
    s = f"{name} {cnt}"
    D.text((rx, ry + 4), s, font=f, fill=(250, 248, 240))
    rx += D.textlength(s, font=f) + 26
text(984, ry + 4, f"{TOTAL} STORIES", F(SANS, 11), fill=(250, 220, 160), anchor="ra")

# ---------------- leads ----------------
LEAD_Y, LEAD_W, GAP = 188, 314, 13
lead_bottom = 0
for i, st in enumerate(STORIES[:3]):
    b = story_cell(st, 28 + i * (LEAD_W + GAP), LEAD_Y, LEAD_W, 76, 16, 10)
    lead_bottom = max(lead_bottom, b)
rule(lead_bottom + 4, wdt=1)

# ---------------- grid rows ----------------
GRID_W = 188
GY = lead_bottom + 12
grid_bottom = 0
for r in range(2):
    row_bottom = 0
    for c in range(5):
        st = STORIES[3 + r * 5 + c]
        b = story_cell(st, 28 + c * (GRID_W + 7), GY + r * 142, GRID_W, 52, 11, 8)
        row_bottom = max(row_bottom, b)
    grid_bottom = GY + r * 142 + (row_bottom - (GY + r * 142))
grid_bottom = max(grid_bottom, GY + 2 * 142)
rule(grid_bottom + 2, wdt=2)

# ---------------- bottom: map + ALSO ----------------
BY = grid_bottom + 8
text(28, BY, "WHERE IT HAPPENED", F(SANS, 12), fill=RED)
MAP_Y = BY + 18
MAP_H = 118
D.rectangle([28, MAP_Y, 388, MAP_Y + MAP_H], fill=(233, 226, 208), outline=INK, width=1)
for gx in range(58, 388, 30):
    D.line([(gx, MAP_Y + 4), (gx, MAP_Y + MAP_H - 4)], fill=(214, 205, 184), width=1)
for gy in range(MAP_Y + 24, MAP_Y + MAP_H, 20):
    D.line([(32, gy), (384, gy)], fill=(214, 205, 184), width=1)
PIN_COLORS = [(23, 58, 94), (38, 84, 124), (20, 92, 60), (146, 96, 20), (108, 40, 120),
              (40, 110, 130), (150, 44, 30), (176, 96, 26), (96, 88, 40), (30, 110, 90),
              (178, 120, 20), (60, 60, 130), (30, 130, 76)]
for st in STORIES:
    px, py = st["pin"]
    mx = 28 + (px - 90) * 0.40
    my = MAP_Y + (py - 215) * 0.34
    my = min(max(my, MAP_Y + 10), MAP_Y + MAP_H - 10)
    col = st.get("color", PIN_COLORS[st["n"] - 1])
    D.ellipse([mx - 8, my - 8, mx + 8, my + 8], fill=col, outline=(250, 248, 240), width=1)
    D.text((mx, my - 6), str(st["n"]), font=F(SANS, 9), fill=(250, 248, 240), anchor="ma")
text(28, MAP_Y + MAP_H + 4, "Numbers match the stories above.", F(SANS_R, 8), fill=FAINT)

AX = 404
text(AX, BY, "ALSO THURSDAY", F(SANS, 12), fill=RED)
ay = BY + 19
bf = F(SERIF_R, 9)
rf = F(SANS, 8)
overwide = []
for region, brief in ALSO:
    D.text((AX, ay), region, font=rf, fill=RED)
    wdt = D.textlength(brief, font=bf)
    if wdt > 996 - (AX + 78):
        overwide.append((region, int(wdt)))
    D.text((AX + 78, ay - 1), brief, font=bf, fill=(52, 48, 42))
    ay += 11
also_bottom = ay

# ---------------- date check + footer ----------------
FOOT = max(also_bottom + 6, MAP_Y + MAP_H + 20)
rule(FOOT, wdt=1)
text(28, FOOT + 4, "DATE CHECK — Voyager's first full light-day of data landed Thursday; the light-day milestone itself was Wednesday, so it is filed as a follow-up, not a Thursday event.",
     F(SANS_R, 8), fill=FAINT)
text(28, FOOT + 16, "All 13 scenes are original illustrations generated for this edition; every headline, deck and figure is typeset from the day's reporting.",
     F(SANS_R, 8), fill=FAINT)
text(996, FOOT + 16, "THE GLOBAL LEDGER · ONE DAY, ONE PAGE", F(SANS, 8), fill=FAINT, anchor="ra")

print("layout: leads end", lead_bottom, "| grid end", grid_bottom, "| also end", also_bottom, "| footer", FOOT + 24)
print("layout overflow:", "FAIL" if FOOT + 24 > 1022 else "ok", "| overwide briefs:", overwide)

out = os.path.join(BASE, "entry.png")
IMG.save(out)
cols = IMG.getcolors(W * H)
print("saved", out, os.path.getsize(out), "bytes;", len(cols), "unique colours")
print("GATE:", "PASS" if (len(cols) >= 18000 and os.path.getsize(out) >= 350 * 1024) else "FAIL",
      "(need >= 18000 colours and >= 358400 bytes)")
