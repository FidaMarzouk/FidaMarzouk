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
    return [f'<text x="48" y="{y}" font-size="14" font-weight="700" letter-spacing="3" fill="{c["text"]}">{left}</text>',
            f'<text x="1152" y="{y}" font-size="14" text-anchor="end" fill="{c["muted"]}">{right}</text>']


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
          f'<text x="68" y="45" font-size="14" font-weight="700" letter-spacing="3" fill="{c["text"]}">OPEN TO END-OF-STUDY INTERNSHIPS</text>',
          f'<text x="1152" y="45" font-size="15" text-anchor="end" fill="{c["muted"]}">Tunis, Tunisia · @{LOGIN}</text>',
          f'<line x1="48" y1="66" x2="1152" y2="66" stroke="{c["rule"]}" stroke-width="2"/>',
          f'<text class="fade" x="48" y="114" font-size="15" font-weight="700" letter-spacing="3" fill="{c["orange"]}">M.SC. BIG DATA ANALYTICS · IHEC CARTHAGE</text>',
          f'<text class="fade" style="animation-delay:.1s" x="44" y="200" font-family="{SERIF}" font-size="80" fill="{c["text"]}">Fida Marzouk</text>',
          f'<text class="fade" style="animation-delay:.2s" font-family="{SERIF}" font-style="italic" font-size="25" fill="{c["blue"]}">'
          f'<tspan x="48" y="250">I build AI/ML systems for real business problems,</tspan>'
          f'<tspan x="48" y="282">and the evaluation that keeps them honest.</tspan></text>',
          f'<line x1="700" y1="96" x2="700" y2="290" stroke="{c["rule"]}"/>']
    for i, (num, label, col) in enumerate(figs):
        x = 740 + i * 222
        y = 210
        s.append(f'<g class="fade" style="animation-delay:{.35+i*.12:.2f}s">'
                 f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="72" fill="{c["text"]}">{num}</text>'
                 f'<rect x="{x}" y="{y+25}" width="10" height="10" rx="2" fill="{c[col]}"/>'
                 f'<text x="{x+16}" y="{y+35}" font-size="13" letter-spacing="0.8" fill="{c["muted"]}">{label}</text></g>')
    s += [f'<line x1="48" y1="320" x2="1152" y2="320" stroke="{c["rule"]}"/>',
          f'<text x="1152" y="350" font-size="14" text-anchor="end" fill="{c["muted"]}">github.com/{LOGIN}</text>',
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
    rowh, y0 = 72, 72
    Hh = y0 + rowh * len(TOOLKIT) + 20
    s = svg_open(1200, Hh, c) + header(c, "THE TOOLKIT", "Technical skills")
    k = 0
    for r, (sector, col, items) in enumerate(TOOLKIT):
        y = y0 + r * rowh
        s += [f'<line x1="48" y1="{y}" x2="1152" y2="{y}" stroke="{c["rule"]}"/>',
              f'<rect x="48" y="{y+21}" width="4" height="30" rx="2" fill="{c[col]}"/>',
              f'<text x="64" y="{y+43}" font-family="{SERIF}" font-size="23" fill="{c["text"]}">{sector}</text>']
        x = 360
        for it in items:
            w = len(it) * 9.0 + 32
            s.append(f'<g class="fade" style="animation-delay:{.1+k*.03:.2f}s"><rect x="{x:.0f}" y="{y+18}" width="{w:.0f}" height="36" rx="18" fill="{c["panel"]}" stroke="{c[col]}" stroke-opacity=".7"/>'
                     f'<text x="{x+w/2:.0f}" y="{y+41}" font-size="16" text-anchor="middle" fill="{c["text"]}">{it}</text></g>')
            x += w + 12
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
    W, Hh = 1200, 312
    gx, gy, cell, step = 112, 120, 15, 19
    s = svg_open(W, Hh, c)
    s += header(c, f'CONTRIBUTIONS · <tspan fill="{c["yellow"]}">{year}</tspan>', "Activity on github.com/" + LOGIN)
    unit = "contribution" if total == 1 else "contributions"
    if total:
        bits = [f'<tspan font-family="{SERIF}" font-size="26" fill="{c["text"]}">{total}</tspan> {unit} in {year}',
                f'{active} active day{"s" if active != 1 else ""}']
        if top and top[1] > 1:
            bits.append(f'busiest day <tspan fill="{c["yellow"]}">{top[0].strftime("%-d %b")}</tspan> ({top[1]})')
        if streak > 1:
            bits.append(f'longest streak {streak} days')
        line = '   ·   '.join(bits)
    else:
        line = f'<tspan font-family="{SERIF}" font-size="26" fill="{c["text"]}">0</tspan> public contributions in {year}'
    s.append(f'<text class="fade" x="48" y="82" font-size="16" fill="{c["muted"]}">{line}</text>')

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
                s.append(f'<text x="{x}" y="{gy-10}" font-size="14" fill="{c["muted"]}">{d.strftime("%b")}</text>')
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
        s.append(f'<text x="{gx-14}" y="{gy + r*step + 13}" font-size="14" text-anchor="end" fill="{c["muted"]}">{lab}</text>')
    # the twist: a scanner beam sweeps the year as the cells pop in
    s.append(f'<rect class="scan" x="{gx-6}" y="{gy-4}" width="3" height="{7*step+4}" rx="1.5" fill="{c["blue"]}"/>')
    if not total:
        s.append(f'<text class="fade" style="animation-delay:1.4s" x="{gx + 26*step}" y="{gy + 3.5*step + 6}" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="22" fill="{c["muted"]}">A quiet year on GitHub</text>')
    ly = gy + 7 * step + 26
    s.append(f'<text x="{gx}" y="{ly+12}" font-size="14" fill="{c["muted"]}">Green follows GitHub\'s contribution scale · <tspan fill="{c["yellow"]}">yellow</tspan> marks the busiest day</text>')
    lx = 1152 - 5 * 19 - 44
    s.append(f'<text x="{lx-8}" y="{ly+12}" font-size="14" text-anchor="end" fill="{c["muted"]}">Less</text>')
    for i, f in enumerate([c["empty"]] + c["g"]):
        s.append(f'<rect x="{lx + i*19}" y="{ly}" width="{cell}" height="{cell}" rx="3" fill="{f}"/>')
    s.append(f'<text x="{lx + 5*19 + 6}" y="{ly+12}" font-size="14" fill="{c["muted"]}">More</text>')
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
    ey0, eh = 350, 112
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
        ty = ay - 84 if up else ay + 48
        tick = (ay - 34, ay - 8) if up else (ay + 8, ay + 30)
        now = when == "NOW"
        s.append(f'<g class="fade" style="animation-delay:{d+.1:.2f}s">'
                 f'<line x1="{x:.0f}" y1="{tick[0]}" x2="{x:.0f}" y2="{tick[1]}" stroke="{c["rule"]}"/>'
                 f'<text x="{x:.0f}" y="{ty}" text-anchor="middle" font-size="13" font-weight="700" letter-spacing="2" fill="{c[col] if now else c["muted"]}">{when}</text>'
                 f'<text x="{x:.0f}" y="{ty+23}" text-anchor="middle" font-family="{SERIF}" font-size="18" fill="{c["text"]}">{title}</text>'
                 f'<text x="{x:.0f}" y="{ty+43}" text-anchor="middle" font-size="13.5" fill="{c["muted"]}">{sub}</text></g>')
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
                 f'<text x="48" y="{y+16}" font-size="14" font-weight="700" letter-spacing="1.5" fill="{c["muted"]}">{yrs}</text>'
                 f'<rect x="146" y="{y-2}" width="8" height="24" rx="2" fill="{c[col]}"/>'
                 f'<text x="176" y="{y+18}" font-family="{SERIF}" font-size="23" xml:space="preserve">{head}</text>'
                 f'<text x="176" y="{y+48}" font-size="16" fill="{c["text"]}" fill-opacity=".86">{l1}</text>'
                 + (f'<text x="176" y="{y+73}" font-size="16" fill="{c["muted"]}">{l2}</text>' if l2 else '') + '</g>')
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
[![Portfolio](https://img.shields.io/badge/Portfolio-fidamarzouk.github.io-bc4c00?style=flat-square&logo=googlechrome&logoColor=white)](https://fidamarzouk.github.io)

{pic('toolkit', 'Technical skills. Programming languages: Python, Java, JavaScript, SQL. AI and data science: Machine Learning, NLP, LLM, RAG. Big data: Hadoop, Hive, Pig, Spark, ELK Stack. DevOps and tools: Git, Docker, Tekton. Web development: ReactJS, Node.js.')}

{contrib_md}

{pic('route', route_alt)}

**Repositories:** {' · '.join(f'[{n}](https://github.com/{LOGIN}/{r})' for n, r in REPOS)}
"""
open(os.path.join(OUT, "README.md"), "w").write(readme)
print("ok", YEARS)
