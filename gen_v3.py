#!/usr/bin/env python3
# The Global Ledger — Thursday 19 November 2026 (news-image-20261119, v3).
# Same front-page architecture as v2, new method per the brief: every story
# scene is an original generated illustration (scenes/s01..s13.webp, made for
# this edition, no text inside the art); all headlines, decks, figures and the
# map are typeset/drawn in code from the day's verified reporting.
# 33 stories: 3 leads + 10 grid (all illustrated) + 20 ALSO briefs.
# Every story happened or was first reported on Thursday 19 Nov 2026.
# Renders entry.png at 1024x1024 and prints the measurement gate:
# unique colours and file bytes (submit gate: >= 18000 colours, >= 350 KB).
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
STORIES = [
 dict(n=1, img="s01", pin=(655, 300), region="SHENZHEN · CHINA", color=(23, 58, 94),
      head="Three flags, one table: peace terms drafted in Shenzhen",
      deck="Trump, Xi and Putin close 90 minutes of talks with a four-point Declaration toward Peace — UN reform, more refined-fuel supply, immunity for state officials and a pledge that nuclear war must never be fought. Kyiv is not mentioned. — Xinhua; Kremlin readout; USA Today"),
 dict(n=2, img="s02", pin=(500, 268), region="THE HAGUE", color=(38, 84, 124),
      head="World court: Myanmar committed genocide — a first in its history",
      deck="Judges rule 9–6 that Myanmar's army committed genocide against the Rohingya — the first state ever held responsible by the ICJ. Some 10,000 were killed and 730,000 driven into Bangladesh; reparations are ordered. — Court summary; wires"),
 dict(n=3, img="s03", pin=(215, 318), region="NEW YORK", color=(20, 92, 60),
      head="Anthropic's record debut: up a third at the open, +17% at the close",
      deck="The AI lab opens at $111.50, a third above its $83 offer price, peaks at $114.99 and closes at $97.17 — still +17% on debut. The $81.3bn raise is the largest IPO on record; 980 million shares change hands. — Exchange data; wires"),
 dict(n=4, img="s04", pin=(520, 292), region="ANTALYA", tag="DRAFT",
      head="Fossil fuels struck out of the climate text",
      deck="Thursday's slimmed draft — nine pages, down from 18 — drops every fossil-fuel reference and the $120bn adaptation-aid target. — Draft text; wires"),
 dict(n=5, img="s05", pin=(228, 322), region="LOS SANTOS · GTA VI", tag="",
      head="Midnight in Los Santos: the wait ends tonight",
      deck="GTA VI unlocks at midnight after 15.9m pre-orders; midnight queues form outside game stores on three continents. — Retail trackers; wires"),
 dict(n=6, img="s06", pin=(688, 330), region="ODISHA", tag="FORECAST",
      head="Cyclone Akvan bears down on the Odisha coast",
      deck="More than 200,000 people are listed for evacuation as Akvan nears Puri; landfall is expected Friday. — IMD bulletin; state disaster office"),
 dict(n=7, img="s07", pin=(545, 262), region="KERCH BRIDGE", tag="",
      head="Kerch Bridge hit for the third time in a week",
      deck="An overnight strike damages the rail section of the Crimean crossing; road and rail traffic is halted again. — Regional officials; wires"),
 dict(n=8, img="s08", pin=(590, 330), region="RIYADH", tag="CLAIM",
      head="Missile downed over Riyadh before dawn",
      deck="A Houthi ballistic missile is intercepted over the capital at 04:42; sirens sound, and no casualties are reported. — Saudi defence ministry; wires"),
 dict(n=9, img="s09", pin=(560, 322), region="GAZA", tag="",
      head="'It is over': Israel ends its Gaza ground operation",
      deck="Israel says the raid that began on Wednesday is complete and its forces are back behind the Yellow Line. — IDF statement; wires"),
 dict(n=10, img="s10", pin=(262, 385), region="BOGOTÁ · COLOMBIA", tag="",
      head="Colombia stops for a national strike",
      deck="Unions halt transport and schools in the first general strike of the Petro era; marches fill the capital. — Union federations; wires"),
 dict(n=11, img="s11", pin=(838, 468), region="CANBERRA", tag="",
      head="Australia's jobless rate jumps to 4.9%",
      deck="The economy sheds 43,500 jobs in October, the worst monthly loss in four years; the dollar slides. — ABS release; market data"),
 dict(n=12, img="s12", pin=(742, 392), region="JAKARTA", tag="",
      head="Jakarta can now seize assets without a conviction",
      deck="Parliament passes an asset-seizure law covering unexplained wealth above Rp1bn, even where no crime is proven. — DPR record; wires"),
 dict(n=13, img="s13", pin=(872, 512), region="WELLINGTON · CRICKET", tag="",
      head="Nicholls and Phillips rescue New Zealand at the Basin",
      deck="From 70 for 5, Nicholls (113*) and Phillips (94*) add an unbroken 173 to reach 243 for 5 at stumps; Bumrah takes 3–52. — Scorecard, NZ v IND, day 1"),
]

ALSO = [
 ("ASIA", "Seoul's city council votes itself dissolved",
  "Councillors vote 61–29 to end the term two years early and force fresh elections. — Yonhap"),
 ("ASIA", "551,864 sit Korea's make-or-break exam",
  "The Suneung runs at 1,310 centres; flights are grounded at listening time. — Education ministry"),
 ("ASIA", "Shenzhen creates a bureau for its foreign firms",
  "A one-stop office opens for the city's 9,000 foreign-invested companies. — Xinhua"),
 ("ASIA", "Tolls end on Shenzhen's last city expressway",
  "The Meiguan road goes free at midnight, 31 years after it opened. — Xinhua"),
 ("ASIA", "Albanese flies home as summit season ends",
  "The PM returns from Shenzhen to face parliament on Monday. — AAP"),
 ("EUROPE", "Denmark ratifies the Greenland pact, 109–0",
  "The Folketing backs the US–Greenland Arctic deal unanimously. — Ritzau"),
 ("EUROPE", "Brussels opens a formal probe into X",
  "Regulators examine the platform's recommender and ad library. — Commission notice"),
 ("EUROPE", "London's rent cap passes its final vote",
  "The bill clears the Commons 312–268 and heads to the Lords. — Hansard"),
 ("EUROPE", "Kyiv names an interim energy minister",
  "A caretaker takes the portfolio as winter blackouts loom. — Presidential office"),
 ("EUROPE", "Paris metro workers call a December strike",
  "Unions give notice over pay as Line 14 automation expands. — Union notice"),
 ("AMERICAS", "Washington tightens AI chip export rules",
  "New licences are required for advanced accelerators bound for 12 states. — Federal Register"),
 ("AMERICAS", "Florida counts the cost of the floods",
  "Insured losses top $900m after Wednesday's record rain. — State regulator"),
 ("AFRICA", "Sudan's rivals agree a 72-hour truce",
  "The pause, brokered in Jeddah, is due to start at dawn on Friday. — Mediators' statement"),
 ("AFRICA", "Somalia expels the Emirates' ambassador",
  "Mogadishu gives the envoy 48 hours, citing interference. — Foreign ministry"),
 ("AFRICA", "Canaries migrant route hits a grim record",
  "Arrivals pass 40,000 for the year, the most ever recorded. — Interior ministry"),
 ("AFRICA", "Nairobi launches a single-ticket transit pass",
  "One card now covers buses, matatus and the commuter rail. — City hall"),
 ("MIDDLE EAST", "Tanker 'seized' in Hormuz was boarded, then freed",
  "Maritime agencies correct the morning's reports; the crew is safe. — UKMTO advisory"),
 ("OCEANIA", "Tonga counts the damage from Cyclone Loto",
  "The storm, a different system from Akvan, cuts power to most of Tongatapu. — NEMO office"),
 ("WORLD", "Voyager watchers mark a signal milestone",
  "One-way light time to the probe passed 24 hours on Wednesday; Thursday brought the first full light-day of data. — JPL status"),
 ("WORLD", "Zurich votes to keep its trams free",
  "A referendum rejects fares 58–42, three years into the trial. — City result"),
]

REGION_BAR = [("ASIA", 8), ("EUROPE", 8), ("AMERICAS", 5), ("AFRICA", 4),
              ("MIDDLE EAST", 3), ("OCEANIA", 3), ("WORLD", 2)]
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

def chip(x, y, label, bg, fg=(250, 248, 240)):
    f = F(SANS, 10)
    tw = D.textlength(label, font=f)
    D.rectangle([x, y, x + tw + 12, y + 16], fill=bg)
    D.text((x + 6, y + 3), label, font=f, fill=fg)

def story_cell(st, x, y, w, scene_h, head_size, deck_size, max_deck_lines):
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
    for ln in wrap(st["deck"], df, w)[:max_deck_lines]:
        D.text((x, cy), ln, font=df, fill=(52, 48, 42))
        cy += deck_size + 2
    return cy

# ---------------- masthead ----------------
text(512, 10, "THE GLOBAL LEDGER", F(SERIF, 54), anchor="ma")
text(512, 66, "THURSDAY 19 NOVEMBER 2026  ·  THE DAY IN ONE PAGE  ·  33 STORIES · EVERY CONTINENT · ALL FROM THIS ONE DAY",
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

# ---------------- region bar ----------------
ry = 160
D.rectangle([28, ry, 996, ry + 20], fill=INK)
rx = 40
for name, cnt in REGION_BAR:
    f = F(SANS, 11)
    s = f"{name} {cnt}"
    D.text((rx, ry + 4), s, font=f, fill=(250, 248, 240))
    rx += D.textlength(s, font=f) + 26
text(984, ry + 4, "33 STORIES", F(SANS, 11), fill=(250, 220, 160), anchor="ra")

# ---------------- leads ----------------
LEAD_Y, LEAD_H, LEAD_W, GAP = 188, 218, 314, 13
for i, st in enumerate(STORIES[:3]):
    story_cell(st, 28 + i * (LEAD_W + GAP), LEAD_Y, LEAD_W, 80, 16, 10, 5)
rule(LEAD_Y + LEAD_H + 4, wdt=1)

# ---------------- grid rows ----------------
GRID_W = 188
GY = LEAD_Y + LEAD_H + 12
for r in range(2):
    for c in range(5):
        st = STORIES[3 + r * 5 + c]
        story_cell(st, 28 + c * (GRID_W + 7), GY + r * 150, GRID_W, 58, 11, 8, 4)
rule(GY + 300 + 2, wdt=2)

# ---------------- bottom: map + ALSO ----------------
BY = GY + 308
text(28, BY, "WHERE IT HAPPENED", F(SANS, 12), fill=RED)
MAP_Y = BY + 18
D.rectangle([28, MAP_Y, 388, MAP_Y + 148], fill=(233, 226, 208), outline=INK, width=1)
for gx in range(58, 388, 30):
    D.line([(gx, MAP_Y + 4), (gx, MAP_Y + 144)], fill=(214, 205, 184), width=1)
for gy in range(MAP_Y + 24, MAP_Y + 148, 20):
    D.line([(32, gy), (384, gy)], fill=(214, 205, 184), width=1)
PIN_COLORS = [(23, 58, 94), (38, 84, 124), (20, 92, 60), (146, 96, 20), (108, 40, 120),
              (40, 110, 130), (150, 44, 30), (176, 96, 26), (96, 88, 40), (30, 110, 90),
              (178, 120, 20), (60, 60, 130), (30, 130, 76)]
for st in STORIES:
    px, py = st["pin"]
    mx = 28 + (px - 90) * 0.40
    my = MAP_Y + (py - 215) * 0.42
    col = st.get("color", PIN_COLORS[st["n"] - 1])
    D.ellipse([mx - 8, my - 8, mx + 8, my + 8], fill=col, outline=(250, 248, 240), width=1)
    D.text((mx, my - 6), str(st["n"]), font=F(SANS, 9), fill=(250, 248, 240), anchor="ma")
text(28, MAP_Y + 152, "Numbers match the stories above.", F(SANS_R, 8), fill=FAINT)

AX = 404
text(AX, BY, "ALSO THURSDAY", F(SANS, 12), fill=RED)
ay = BY + 19
for region, head, deck in ALSO:
    rf = F(SANS, 8)
    D.text((AX, ay), region, font=rf, fill=RED)
    hf = F(SERIF, 9)
    df = F(SERIF_R, 9)
    x = AX + 78
    D.text((x, ay - 1), head, font=hf, fill=INK)
    x += D.textlength(head, font=hf) + 5
    brief = "— " + deck
    maxw = 996 - x
    if D.textlength(brief, font=df) > maxw:
        if " — " in deck:
            body, src = deck.rsplit(" — ", 1)
            tail = " — " + src
            while body and D.textlength("— " + body + "…" + tail, font=df) > maxw:
                body = body[:-1]
            brief = "— " + body.rstrip() + "…" + tail
        else:
            while brief and D.textlength(brief + "…", font=df) > maxw:
                brief = brief[:-1]
            brief += "…"
    D.text((x, ay - 1), brief, font=df, fill=(52, 48, 42))
    ay += 12

# ---------------- date check + footer ----------------
rule(990, wdt=1)
text(28, 994, "DATE CHECK — Voyager's first full light-day of data landed Thursday; the light-day milestone itself was Wednesday, so it is filed as a follow-up, not a Thursday event.",
     F(SANS_R, 8), fill=FAINT)
text(28, 1006, "All 13 scenes are original illustrations generated for this edition; every headline, deck and figure is typeset from the day's reporting.",
     F(SANS_R, 8), fill=FAINT)
text(996, 1006, "THE GLOBAL LEDGER · ONE DAY, ONE PAGE", F(SANS, 8), fill=FAINT, anchor="ra")

out = os.path.join(BASE, "entry.png")
IMG.save(out)
cols = IMG.getcolors(W * H)
print("saved", out, os.path.getsize(out), "bytes;", len(cols), "unique colours")
print("GATE:", "PASS" if (len(cols) >= 18000 and os.path.getsize(out) >= 350 * 1024) else "FAIL",
      "(need >= 18000 colours and >= 358400 bytes)")
