"""Generates Fida's GitHub profile README: cover, toolkit, contribution grids per year, route timeline
(each as dark + light SVG), README.md and a GitHub-style preview.html."""
import base64, datetime as dt, json, os, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("OUT_DIR", HERE)  # repo root on GitHub; a scratch folder for local previews
os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)

LOGIN = "FidaMarzouk"
# Day-level public contributions per calendar year (from github.com/users/<login>/contributions).
DATA = json.load(open(os.path.join(HERE, "data", "contributions.json")))
CONTRIB = DATA["years"]
YEARS = sorted(CONTRIB, reverse=True)

THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", rule="#30363d", text="#e6edf3", muted="#8b949e",
                 green="#3fb950", blue="#58a6ff", orange="#f0883e", yellow="#e3b341", purple="#a371f7",
                 empty="#161b22", g=["#0e4429", "#006d32", "#26a641", "#39d353"]),
    "light": dict(bg="#ffffff", panel="#f6f8fa", rule="#d0d7de", text="#1f2328", muted="#59636e",
                  green="#1a7f37", blue="#0969da", orange="#bc4c00", yellow="#bf8700", purple="#8250df",
                  empty="#ebedf0", g=["#9be9a8", "#40c463", "#30a14e", "#216e39"]),
}
SERIF = "Georgia, 'Times New Roman', serif"
SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

ANIM = """<style>
 .fade{animation:fade .8s ease-out both}
 .pop{transform-box:fill-box;transform-origin:center;animation:pop .45s cubic-bezier(.3,1.6,.5,1) both}
 .draw{stroke-dasharray:1200;stroke-dashoffset:1200;animation:draw 1.6s ease-out .1s forwards}
 .scan{animation:scan 1.5s cubic-bezier(.4,0,.2,1) .05s both}
 .pulse{transform-box:fill-box;transform-origin:center;animation:pulse 1.4s ease-out 1.7s 3 both}
 @keyframes fade{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
 @keyframes pop{0%{opacity:0;transform:scale(.2)}100%{opacity:1;transform:scale(1)}}
 @keyframes draw{to{stroke-dashoffset:0}}
 @keyframes scan{0%{opacity:0;transform:translateX(0)}10%{opacity:.9}85%{opacity:.9}100%{opacity:0;transform:translateX(1010px)}}
 @keyframes pulse{0%{opacity:.9;transform:scale(1)}100%{opacity:0;transform:scale(2.4)}}
 @media (prefers-reduced-motion: reduce){.fade,.pop,.scan,.pulse{animation:none}.draw{animation:none;stroke-dashoffset:0}.scan,.pulse{opacity:0}}
</style>"""


def svg_open(W, Hh, c):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Hh}" viewBox="0 0 {W} {Hh}" font-family="{SANS}">',
            ANIM, f'<rect width="{W}" height="{Hh}" rx="10" fill="{c["bg"]}"/>']


def header(c, left, right, y=44):
    return [f'<text x="48" y="{y}" font-size="12" font-weight="700" letter-spacing="3" fill="{c["text"]}">{left}</text>',
            f'<text x="1152" y="{y}" font-size="12" text-anchor="end" fill="{c["muted"]}">{right}</text>']


# ---------------------------------------------------------------- cover
PUBLIC_REPOS = DATA["public_repos"]
UPDATED = dt.date.fromisoformat(DATA["updated"])


def cover(t):
    c = THEMES[t]
    W, Hh = 1200, 380
    cur = YEARS[0]
    figs = [(str(year_stats(cur)[1]), f"CONTRIBUTIONS IN {cur}", "green"), (str(PUBLIC_REPOS), "PUBLIC REPOSITORIES", "blue")]
    s = svg_open(W, Hh, c)
    s += [f'<circle cx="54" cy="40" r="5" fill="{c["green"]}"/>',
          f'<circle class="pulse" cx="54" cy="40" r="5" fill="none" stroke="{c["green"]}" stroke-width="2"/>',
          f'<text x="68" y="44" font-size="12" font-weight="700" letter-spacing="3" fill="{c["text"]}">OPEN TO END-OF-STUDY INTERNSHIPS</text>',
          f'<text x="1152" y="44" font-size="13" text-anchor="end" fill="{c["muted"]}">Tunis, Tunisia · @{LOGIN}</text>',
          f'<line x1="48" y1="66" x2="1152" y2="66" stroke="{c["rule"]}" stroke-width="2"/>',
          f'<text class="fade" x="48" y="114" font-size="13" font-weight="700" letter-spacing="3" fill="{c["orange"]}">M.SC. BIG DATA ANALYTICS · IHEC CARTHAGE</text>',
          f'<text class="fade" style="animation-delay:.1s" x="44" y="200" font-family="{SERIF}" font-size="80" fill="{c["text"]}">Fida Marzouk</text>',
          f'<text class="fade" style="animation-delay:.2s" font-family="{SERIF}" font-style="italic" font-size="22" fill="{c["blue"]}">'
          f'<tspan x="48" y="248">I build AI/ML systems for real business problems,</tspan>'
          f'<tspan x="48" y="277">and the evaluation that keeps them honest.</tspan></text>',
          f'<line x1="700" y1="96" x2="700" y2="290" stroke="{c["rule"]}"/>']
    for i, (num, label, col) in enumerate(figs):
        x = 744 + i * 220
        y = 210
        s.append(f'<g class="fade" style="animation-delay:{.35+i*.12:.2f}s">'
                 f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="64" fill="{c["text"]}">{num}</text>'
                 f'<rect x="{x}" y="{y+24}" width="8" height="8" rx="2" fill="{c[col]}"/>'
                 f'<text x="{x+14}" y="{y+32}" font-size="10" letter-spacing="1.5" fill="{c["muted"]}">{label}</text></g>')
    s += [f'<line x1="48" y1="320" x2="1152" y2="320" stroke="{c["rule"]}"/>',
          f'<text x="48" y="348" font-size="12" fill="{c["muted"]}">Updated {UPDATED.strftime("%-d %B %Y")} from GitHub activity</text>',
          f'<text x="1152" y="348" font-size="12" text-anchor="end" fill="{c["muted"]}">github.com/{LOGIN}</text>',
          '</svg>']
    return "\n".join(s)


# ---------------------------------------------------------------- toolkit
TOOLKIT = [
    ("Programming Languages", "blue", ["Python", "Java", "JavaScript", "SQL"]),
    ("AI &amp; Data Science", "green", ["Machine Learning", "NLP", "LLM", "RAG"]),
    ("Big Data", "orange", ["Hadoop", "Hive", "Pig", "Spark", "ELK Stack"]),
    ("DevOps &amp; Tools", "yellow", ["Git", "Docker", "Tekton"]),
    ("Web Development", "purple", ["ReactJS", "Node.js"]),
]


def toolkit(t):
    c = THEMES[t]
    rowh, y0 = 66, 70
    Hh = y0 + rowh * len(TOOLKIT) + 20
    s = svg_open(1200, Hh, c) + header(c, "THE TOOLKIT", "Technical skills")
    k = 0
    for r, (sector, col, items) in enumerate(TOOLKIT):
        y = y0 + r * rowh
        s += [f'<line x1="48" y1="{y}" x2="1152" y2="{y}" stroke="{c["rule"]}"/>',
              f'<rect x="48" y="{y+20}" width="4" height="26" rx="2" fill="{c[col]}"/>',
              f'<text x="64" y="{y+39}" font-family="{SERIF}" font-size="20" fill="{c["text"]}">{sector}</text>']
        x = 320
        for it in items:
            w = len(it) * 7.4 + 26
            s.append(f'<g class="fade" style="animation-delay:{.1+k*.03:.2f}s"><rect x="{x:.0f}" y="{y+17}" width="{w:.0f}" height="30" rx="15" fill="{c["panel"]}" stroke="{c[col]}" stroke-opacity=".7"/>'
                     f'<text x="{x+w/2:.0f}" y="{y+37}" font-size="13" text-anchor="middle" fill="{c["text"]}">{it}</text></g>')
            x += w + 10
            k += 1
    s += [f'<line x1="48" y1="{y0+rowh*len(TOOLKIT)}" x2="1152" y2="{y0+rowh*len(TOOLKIT)}" stroke="{c["rule"]}"/>', '</svg>']
    return "\n".join(s)


# ---------------------------------------------------------------- contribution grid
def year_stats(year):
    days = {dt.date.fromisoformat(k): v for k, v in CONTRIB[year].items()}
    total = sum(days.values())
    streak = best = 0
    prev = None
    for d in sorted(days):
        streak = streak + 1 if prev and (d - prev).days == 1 else 1
        best = max(best, streak)
        prev = d
    top = max(days.items(), key=lambda x: x[1]) if days else None
    return days, total, len(days), best, top


def level(v):
    return 0 if v <= 3 else 1 if v <= 7 else 2 if v <= 12 else 3


def grid(year, t):
    c = THEMES[t]
    y = int(year)
    days, total, active, streak, top = year_stats(year)
    W, Hh = 1200, 300
    gx, gy, cell, step = 112, 112, 15, 19
    s = svg_open(W, Hh, c)
    s += header(c, f'CONTRIBUTIONS · <tspan fill="{c["yellow"]}">{year}</tspan>', "Activity on github.com/" + LOGIN)
    unit = "contribution" if total == 1 else "contributions"
    if total:
        bits = [f'<tspan font-family="{SERIF}" font-size="22" fill="{c["text"]}">{total}</tspan> {unit} in {year}',
                f'{active} active day{"s" if active != 1 else ""}']
        if top and top[1] > 1:
            bits.append(f'busiest day <tspan fill="{c["yellow"]}">{top[0].strftime("%-d %b")}</tspan> ({top[1]})')
        if streak > 1:
            bits.append(f'longest streak {streak} days')
        line = '   ·   '.join(bits)
    else:
        line = f'<tspan font-family="{SERIF}" font-size="22" fill="{c["text"]}">0</tspan> public contributions in {year}'
    s.append(f'<text class="fade" x="48" y="80" font-size="13" fill="{c["muted"]}">{line}</text>')

    jan1 = dt.date(y, 1, 1)
    start = jan1 - dt.timedelta(days=(jan1.weekday() + 1) % 7)  # Sunday on/before Jan 1
    end = dt.date(y, 12, 31)
    d = start
    months_done = set()
    while d <= end:
        col = (d - start).days // 7
        row = (d.weekday() + 1) % 7
        if d.year == y:
            x, yy = gx + col * step, gy + row * step
            v = days.get(d, 0)
            if d.day <= 7 and d.month not in months_done and row == 0 or (d == jan1 and 1 not in months_done):
                months_done.add(d.month)
                s.append(f'<text x="{x}" y="{gy-10}" font-size="11" fill="{c["muted"]}">{d.strftime("%b")}</text>')
            is_top = top and d == top[0] and v > 1
            fill = c["yellow"] if is_top else (c["empty"] if v == 0 else c["g"][level(v)])
            delay = .05 + col * .022 + row * .03
            title = f'<title>{v} contribution{"s" if v != 1 else ""} on {d.strftime("%-d %B %Y")}</title>' if v else ''
            s.append(f'<rect class="pop" style="animation-delay:{delay:.2f}s" x="{x}" y="{yy}" width="{cell}" height="{cell}" rx="3" fill="{fill}"'
                     f'{"" if v or t == "light" else " stroke=" + chr(34) + c["rule"] + chr(34) + " stroke-opacity=" + chr(34) + ".35" + chr(34)}>{title}</rect>')
            if is_top:
                s.append(f'<rect class="pulse" x="{x}" y="{yy}" width="{cell}" height="{cell}" rx="3" fill="none" stroke="{c["yellow"]}" stroke-width="2"/>')
        d += dt.timedelta(days=1)
    for r, lab in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        s.append(f'<text x="{gx-14}" y="{gy + r*step + 12}" font-size="11" text-anchor="end" fill="{c["muted"]}">{lab}</text>')
    # the twist: a scanner beam sweeps the year as the cells pop in
    s.append(f'<rect class="scan" x="{gx-6}" y="{gy-4}" width="3" height="{7*step+4}" rx="1.5" fill="{c["blue"]}"/>')
    if not total:
        s.append(f'<text class="fade" style="animation-delay:1.4s" x="{gx + 26*step}" y="{gy + 3.5*step + 6}" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="18" fill="{c["muted"]}">A quiet year on GitHub</text>')
    ly = gy + 7 * step + 26
    s.append(f'<text x="{gx}" y="{ly+11}" font-size="11" fill="{c["muted"]}">Green follows GitHub\'s contribution scale · <tspan fill="{c["yellow"]}">yellow</tspan> marks the busiest day</text>')
    lx = 1152 - 5 * 19 - 34
    s.append(f'<text x="{lx-8}" y="{ly+11}" font-size="11" text-anchor="end" fill="{c["muted"]}">Less</text>')
    for i, f in enumerate([c["empty"]] + c["g"]):
        s.append(f'<rect x="{lx + i*19}" y="{ly}" width="{cell}" height="{cell}" rx="3" fill="{f}"/>')
    s.append(f'<text x="{lx + 5*19 + 4}" y="{ly+11}" font-size="11" fill="{c["muted"]}">More</text>')
    s.append('</svg>')
    return "\n".join(s)


# ---------------------------------------------------------------- route
MILESTONES = [  # (when, title, sub, colour)
    ("2022", "B.S. Information Systems", "ISG Sousse", "blue"),
    ("2025", "HRMDSS", "final-year project", "orange"),
    ("2025", "M.Sc. Big Data Analytics", "IHEC Carthage", "blue"),
    ("2026", "Lumina", "AI mental health companion", "green"),
    ("2026", "ElyaEval", "LLM testing framework", "green"),
    ("2026", "RetinaGuard", "screening triage research", "green"),
    ("NOW", "open to internships", "end-of-study · 2027", "yellow"),
]
ENTRIES = [  # (when, title parts, line 1, line 2, colour)
    ("2026", ["RetinaGuard", "Personal research project", "Oct – Nov"],
     "End-to-end triage for retinal fundus photos: retake · refer · no refer · defer to a human, with U-Net lesion maps",
     "Dagster + DVC pipeline over 4 datasets · ConvNeXt, EfficientNet, DINOv2 · AUROC 0.97 external · ONNX + FastAPI", "green"),
    ("2026", ["ElyaEval", "Internship at Elyadata", "Jul – Aug"],
     "Testing framework and CI gate for LLM applications: RAG apps, LLM tasks and tool-calling agents, built on DeepEval",
     "Bootstrap-CI regression gating · judge calibration (Cohen's kappa) · cost budgets · Tekton CI gate · RAG + agent demos", "green"),
    ("2026", ["Lumina", "AI mental health companion", "IHEC · May – Jun"],
     "Layered safety screening: rules · RoBERTa · Llama Guard 3 · LLM risk reader, reaching 97% crisis recall",
     "Intent classifier on agreement-filtered LLM labels · intent- and emotion-aware RAG dialogue over clinical sources", "green"),
    ("2025", ["HRMDSS", "Final-year project at Enova Robotics", "Jan – May"],
     "Full-stack HR platform for leave, attendance, scheduling and internal communication, with a real-time WebSocket inbox",
     "LangGraph RAG assistant in Docker behind an allow-list gateway · prompt-injection screening · LangSmith tracing", "orange"),
]


def route(t):
    c = THEMES[t]
    W = 1200
    ey0, eh = 330, 92
    Hh = ey0 + eh * len(ENTRIES) - 6
    s = svg_open(W, Hh, c) + header(c, "THE ROUTE", "So far, and where it's heading")
    s.append(f'<line x1="48" y1="64" x2="1152" y2="64" stroke="{c["rule"]}"/>')
    ax0, ax1, ay = 70, 1140, 190
    s.append(f'<line class="draw" x1="{ax0}" y1="{ay}" x2="{ax1}" y2="{ay}" stroke="{c["muted"]}" stroke-width="2"/>')
    s.append(f'<path class="fade" style="animation-delay:1.5s" d="M{ax1+4} {ay} l-9 -5 v10 z" fill="{c["muted"]}"/>')
    n = len(MILESTONES)
    for i, (when, title, sub, col) in enumerate(MILESTONES):
        x = ax0 + 50 + i * (ax1 - ax0 - 110) / (n - 1)
        up = i % 2 == 0
        d = .2 + i * .17
        ty = ay - 74 if up else ay + 46
        tick = (ay - 34, ay - 8) if up else (ay + 8, ay + 30)
        now = when == "NOW"
        s.append(f'<g class="fade" style="animation-delay:{d+.1:.2f}s">'
                 f'<line x1="{x:.0f}" y1="{tick[0]}" x2="{x:.0f}" y2="{tick[1]}" stroke="{c["rule"]}"/>'
                 f'<text x="{x:.0f}" y="{ty}" text-anchor="middle" font-size="11" font-weight="700" letter-spacing="2" fill="{c[col] if now else c["muted"]}">{when}</text>'
                 f'<text x="{x:.0f}" y="{ty+20}" text-anchor="middle" font-family="{SERIF}" font-size="15" fill="{c["text"]}">{title}</text>'
                 f'<text x="{x:.0f}" y="{ty+37}" text-anchor="middle" font-size="11" fill="{c["muted"]}">{sub}</text></g>')
        s.append(f'<circle class="pop" style="animation-delay:{d:.2f}s" cx="{x:.0f}" cy="{ay}" r="{7 if now else 6}" fill="{c[col]}" stroke="{c["bg"]}" stroke-width="3"/>')
        if now:
            s.append(f'<circle class="pulse" cx="{x:.0f}" cy="{ay}" r="6" fill="none" stroke="{c[col]}" stroke-width="2"/>')
    s.append(f'<line x1="48" y1="{ey0-30}" x2="1152" y2="{ey0-30}" stroke="{c["rule"]}"/>')
    s.append(f'<line x1="150" y1="{ey0-6}" x2="150" y2="{Hh-26}" stroke="{c["rule"]}"/>')
    for i, (yrs, parts, l1, l2, col) in enumerate(ENTRIES):
        y = ey0 + i * eh
        d = 1.0 + i * .12
        head = f'<tspan fill="{c["text"]}">{parts[0]}</tspan>' + "".join(f'<tspan fill="{c["muted"]}">  ·  {p}</tspan>' for p in parts[1:])
        s.append(f'<g class="fade" style="animation-delay:{d:.2f}s">'
                 f'<text x="48" y="{y+14}" font-size="12" font-weight="700" letter-spacing="1.5" fill="{c["muted"]}">{yrs}</text>'
                 f'<rect x="146" y="{y-2}" width="8" height="20" rx="2" fill="{c[col]}"/>'
                 f'<text x="176" y="{y+15}" font-family="{SERIF}" font-size="19" xml:space="preserve">{head}</text>'
                 f'<text x="176" y="{y+40}" font-size="13.5" fill="{c["text"]}" fill-opacity=".86">{l1}</text>'
                 + (f'<text x="176" y="{y+60}" font-size="13.5" fill="{c["muted"]}">{l2}</text>' if l2 else '') + '</g>')
    s.append('</svg>')
    return "\n".join(s)


# ---------------------------------------------------------------- write assets
files = {"cover": cover, "toolkit": toolkit, "route": route}
for y in YEARS:
    files[f"contributions-{y}"] = (lambda yy: (lambda t: grid(yy, t)))(y)
for name, fn in files.items():
    for t in THEMES:
        open(os.path.join(OUT, "assets", f"{name}-{t}.svg"), "w").write(fn(t))


def pic(name, alt):
    return (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">\n'
            f'  <source media="(prefers-color-scheme: light)" srcset="assets/{name}-light.svg">\n'
            f'  <img alt="{H.escape(alt)}" src="assets/{name}-dark.svg" width="100%">\n</picture>')


REPOS = [("ElyaEval", "DeepEval-based-Testing-Framework-for-LLM-Applications"), ("RAG-Demo", "RAG-Demo"),
         ("Agent-Demo", "Agent-Demo"), ("RetinaGuard", "retinaguard"), ("Lumina", "Lumina"), ("HRMDSS", "HRMDSS")]
INTRO = ("Master’s student in Big Data Analytics, I focus on building AI/ML systems that address real business problems. "
         "I am looking for an opportunity to apply these skills on high-impact projects and sharpen them against real-world constraints.")


def grid_alt(y):
    _, total, active, streak, top = year_stats(y)
    return f"Contribution grid for {y}: {total} public contributions on {active} active days" + (
        f", busiest day {top[0].strftime('%-d %B')} with {top[1]}." if top else ".")


route_alt = "The route: " + "; ".join(f"{w} {t}, {s}" for w, t, s, _ in MILESTONES) + "."
contrib_md = "\n\n".join(
    f"<details{' open' if i == 0 else ''}>\n<summary><b>{y}</b> · {year_stats(y)[1]} contributions</summary>\n\n{pic('contributions-' + y, grid_alt(y))}\n\n</details>"
    for i, y in enumerate(YEARS))

readme = f"""{pic('cover', 'Fida Marzouk, M.Sc. Big Data Analytics student at IHEC Carthage, open to end-of-study internships. I build AI/ML systems for real business problems, and the evaluation that keeps them honest.')}

{INTRO}

[![LinkedIn](https://img.shields.io/badge/LinkedIn-fida--marzouk-0969da?style=flat-square&logo=linkedin&logoColor=white)](https://linkedin.com/in/fida-marzouk)
[![Email](https://img.shields.io/badge/Email-fidamarzouk%40gmail.com-1a7f37?style=flat-square&logo=gmail&logoColor=white)](mailto:fidamarzouk@gmail.com)

{pic('toolkit', 'Technical skills. Programming languages: Python, Java, JavaScript, SQL. AI and data science: Machine Learning, NLP, LLM, RAG. Big data: Hadoop, Hive, Pig, Spark, ELK Stack. DevOps and tools: Git, Docker, Tekton. Web development: ReactJS, Node.js.')}

{contrib_md}

{pic('route', route_alt)}

**Repositories:** {' · '.join(f'[{n}](https://github.com/{LOGIN}/{r})' for n, r in REPOS)}
"""
open(os.path.join(OUT, "README.md"), "w").write(readme)


# ---------------------------------------------------------------- preview page
def uri(name, t):
    return "data:image/svg+xml;base64," + base64.b64encode(open(os.path.join(OUT, "assets", f"{name}-{t}.svg"), "rb").read()).decode()


def img(name, alt):
    return (f'<img class="d" src="{uri(name, "dark")}" alt="{H.escape(alt)}">'
            f'<img class="l" src="{uri(name, "light")}" alt="{H.escape(alt)}">')


contrib_html = "".join(
    f'<details{" open" if i == 0 else ""} name="yr"><summary><b>{y}</b> · {year_stats(y)[1]} contributions</summary>{img("contributions-" + y, grid_alt(y))}</details>'
    for i, y in enumerate(YEARS))
repos_html = " · ".join(f'<a href="https://github.com/{LOGIN}/{r}">{n}</a>' for n, r in REPOS)

preview = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Fida Marzouk · README preview</title>
<style>
:root{{--bg:#0d1117;--bd:#30363d;--tx:#e6edf3;--mu:#8b949e;--ln:#4493f8;--chip:#161b22}}
body.light{{--bg:#ffffff;--bd:#d0d7de;--tx:#1f2328;--mu:#59636e;--ln:#0969da;--chip:#f6f8fa}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--tx);font:14px/1.5 -apple-system,'Segoe UI',Helvetica,Arial,sans-serif;transition:background .2s}}
.bar{{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;max-width:980px;margin:24px auto 12px;padding:0 16px}}
.who{{color:var(--mu)}}.who b{{color:var(--tx)}}
.tg{{display:flex;border:1px solid var(--bd);border-radius:6px;overflow:hidden}}
.tg button{{background:var(--chip);color:var(--tx);border:0;padding:6px 14px;cursor:pointer;font:inherit}}
.tg button.on{{background:#238636;color:#fff}}
.box{{max-width:980px;margin:0 auto 40px;border:1px solid var(--bd);border-radius:6px}}
.hd{{padding:10px 16px;border-bottom:1px solid var(--bd);font-size:12px;color:var(--mu)}}
.md{{padding:24px 32px}}.md img{{width:100%;display:block;border-radius:6px;margin:16px 0}}
body:not(.light) .l, body.light .d{{display:none}}
a{{color:var(--ln);text-decoration:none}}a:hover{{text-decoration:underline}}
.badges{{display:flex;gap:6px;flex-wrap:wrap}}.badge{{font-size:11px;color:#fff !important;text-decoration:none !important;border-radius:3px;padding:2px 8px;font-weight:600}}
details{{margin:4px 0}}summary{{cursor:pointer;padding:4px 0}}details img{{margin-top:8px}}
.hint{{font-size:12px;color:var(--mu);margin:16px 0 4px}}
@media(max-width:600px){{.md{{padding:16px}}}}
</style></head><body>
<div class="bar"><div class="who"><b>FidaMarzouk</b> / README.md · profile preview</div>
<div class="tg"><button class="on" onclick="th(0,this)">Dark</button><button onclick="th(1,this)">Light</button></div></div>
<div class="box"><div class="hd">README.md</div><div class="md">
{img('cover', 'Cover')}
<p>{H.escape(INTRO)}</p>
<div class="badges"><a class="badge" style="background:#0969da" href="https://linkedin.com/in/fida-marzouk" target="_blank" rel="noopener">in LinkedIn · fida-marzouk</a><a class="badge" style="background:#1a7f37" href="mailto:fidamarzouk@gmail.com">✉ Email · fidamarzouk@gmail.com</a></div>
{img('toolkit', 'Toolkit')}
<p class="hint">Click a year to switch (on GitHub these are collapsible rows)</p>
{contrib_html}
{img('route', 'The route')}
<p><b>Repositories:</b> {repos_html}</p>
</div></div>
<script>{{
function replay(root){{root.querySelectorAll('img').forEach(i=>{{const s=i.src;i.src='';i.src=s}})}}
window.th=function(l,b){{document.body.classList.toggle('light',!!l);document.querySelectorAll('.tg button').forEach(x=>x.classList.remove('on'));b.classList.add('on');replay(document)}};
document.querySelectorAll('details').forEach(d=>d.addEventListener('toggle',()=>{{if(d.open){{document.querySelectorAll('details').forEach(o=>{{if(o!==d)o.open=false}});replay(d)}}}}));
}}</script>
</body></html>"""
if os.environ.get("PREVIEW"):
    open(os.path.join(OUT, "preview.html"), "w").write(preview)
print("ok", YEARS)
