#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Minimal Markdown -> styled HTML converter (Persian RTL / English LTR)."""
import re, html, sys

SRC = sys.argv[1]
OUT = sys.argv[2]
LANG = (sys.argv[3] if len(sys.argv) > 3 else "fa").lower()

text = open(SRC, encoding="utf-8").read()
lines = text.split("\n")

NUM_RE = re.compile(
    r"(\$[0-9][0-9.,/–\-]*"
    r"|[0-9][0-9.,/–\-]*(?:ms|s|k|M|B)(?![A-Za-z0-9])"
    r"|[0-9]+(?:\.[0-9]+)?%"
    r"|[0-9]+(?:×|x)[0-9]+)"
)

def inline(s):
    s = html.escape(s, quote=False)
    s = NUM_RE.sub(lambda m: '<span class="num">' + m.group(0) + "</span>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
               r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s

def is_table_sep(line):
    return bool(re.match(r"^\s*\|[\s:\-|]+\|\s*$", line)) and "-" in line

def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]

out, toc = [], []
i = 0
in_list = None
in_quote = False

def close_list():
    global in_list
    if in_list:
        out.append(f"</{in_list}>")
        in_list = None

def close_quote():
    global in_quote
    if in_quote:
        out.append("</blockquote>")
        in_quote = False

while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    if stripped.startswith("```"):
        close_list(); close_quote()
        j, buf = i + 1, []
        while j < len(lines) and not lines[j].strip().startswith("```"):
            buf.append(lines[j]); j += 1
        out.append("<pre><code>" + html.escape("\n".join(buf)) + "</code></pre>")
        i = j + 1
        continue

    if not stripped:
        close_list(); close_quote()
        i += 1
        continue

    m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
    if m:
        close_list(); close_quote()
        level, content = len(m.group(1)), inline(m.group(2))
        if level == 2:
            anchor = "s" + str(len(toc) + 1)
            toc.append((anchor, m.group(2)))
            out.append(f'<h2 id="{anchor}">{content}</h2>')
        else:
            out.append(f"<h{level}>{content}</h{level}>")
        i += 1
        continue

    if re.match(r"^(-{3,}|\*{3,})$", stripped):
        close_list(); close_quote()
        out.append("<hr>")
        i += 1
        continue

    if stripped.startswith("|") and i + 1 < len(lines) and is_table_sep(lines[i + 1]):
        close_list(); close_quote()
        headers = split_row(stripped)
        i += 2
        rows = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            rows.append(split_row(lines[i]))
            i += 1
        out.append("<div class='table-wrap'><table><thead><tr>")
        out += [f"<th>{inline(h)}</th>" for h in headers]
        out.append("</tr></thead><tbody>")
        for r in rows:
            out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
        out.append("</tbody></table></div>")
        continue

    if stripped.startswith(">"):
        if not in_quote:
            close_list()
            out.append("<blockquote>")
            in_quote = True
        out.append("<p>" + inline(stripped[1:].strip()) + "</p>")
        i += 1
        continue
    else:
        close_quote()

    m = re.match(r"^-\s+\[( |x|X)\]\s+(.*)$", stripped)
    if m:
        if in_list != "ul":
            close_list(); out.append("<ul class='check'>"); in_list = "ul"
        mark = "☑" if m.group(1).lower() == "x" else "☐"
        out.append(f"<li>{mark} {inline(m.group(2))}</li>")
        i += 1
        continue

    m = re.match(r"^[-*]\s+(.*)$", stripped)
    if m:
        if in_list != "ul":
            close_list(); out.append("<ul>"); in_list = "ul"
        out.append(f"<li>{inline(m.group(1))}</li>")
        i += 1
        continue

    m = re.match(r"^(\d+)\.\s+(.*)$", stripped)
    if m:
        if in_list != "ol":
            close_list(); out.append("<ol>"); in_list = "ol"
        out.append(f"<li>{inline(m.group(2))}</li>")
        i += 1
        continue

    close_list()
    out.append(f"<p>{inline(stripped)}</p>")
    i += 1

close_list(); close_quote()

dir_attr = "rtl" if LANG == "fa" else "ltr"
title = "نقشهٔ جامع مدل‌های صوتی هوش مصنوعی" if LANG == "fa" else "The Complete Map of AI Audio Models"
toc_label = "فهرست" if LANG == "fa" else "Contents"
nav = ('<nav class="lang"><a class="active" href="index.html">فارسی</a>'
       '<a class="' + ("" if LANG == "fa" else "active") + '" href="en.html">English</a></nav>')
toc_html = "".join(f'<a href="#{a}">{html.escape(t)}</a>' for a, t in toc)

align_css = ""
if LANG != "fa":
    align_css = """
  body { font-family:"Charter","Georgia","Times New Roman",serif; }
  h1,h2,h3,.toc,.lang { font-family:"SF Pro Text","Segoe UI",system-ui,sans-serif; }
  th, td { text-align:left; }
  ul, ol { padding-left:24px; padding-right:0; }
  .lang a.active { background:rgba(110,168,254,.18); }
"""

html_doc = f"""<!DOCTYPE html>
<html lang="{'fa' if LANG=='fa' else 'en'}" dir="{dir_attr}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>
  :root {{
    --bg:#0f1115; --panel:#161922; --ink:#e8eaf0; --muted:#9aa3b2;
    --line:#262b38; --accent:#6ea8fe; --accent2:#8ee6c8; --code:#1d2230;
  }}
  @media (prefers-color-scheme: light) {{
    :root {{ --bg:#fbfbfd; --panel:#fff; --ink:#1a1d24; --muted:#5b6472;
             --line:#e4e7ee; --accent:#2563eb; --accent2:#0f8a6a; --code:#f2f4f8; }}
  }}
  * {{ box-sizing:border-box; }}
  body {{
    margin:0; background:var(--bg); color:var(--ink);
    font-family:"Vazirmatn","IRANSans","SF Pro Text","Segoe UI",Tahoma,sans-serif;
    line-height:1.95; font-size:16px;
  }}
  .wrap {{ max-width:1080px; margin:0 auto; padding:40px 28px 96px; }}
  h1 {{ font-size:2.1rem; line-height:1.5; margin:0 0 6px; letter-spacing:-.5px; }}
  h2 {{ font-size:1.45rem; margin:56px 0 16px; padding-bottom:10px;
        border-bottom:1px solid var(--line); }}
  h3 {{ font-size:1.12rem; margin:32px 0 10px; color:var(--accent); }}
  h1 + h3 {{ color:var(--muted); font-weight:500; font-size:1.02rem; margin-top:0; }}
  p {{ margin:12px 0; }}
  a {{ color:var(--accent); text-decoration:none; border-bottom:1px solid transparent; }}
  a:hover {{ border-bottom-color:var(--accent); }}
  code {{ background:var(--code); padding:2px 6px; border-radius:6px;
          font-family:"SF Mono",ui-monospace,Menlo,monospace; font-size:.88em;
          direction:ltr; unicode-bidi:isolate; display:inline-block; }}
  pre {{ background:var(--code); padding:16px; border-radius:12px; overflow:auto;
         direction:ltr; text-align:left; }}
  pre code {{ background:none; padding:0; }}
  hr {{ border:0; border-top:1px solid var(--line); margin:40px 0; }}
  blockquote {{ margin:22px 0; padding:16px 20px; background:var(--panel);
                border-right:3px solid var(--accent2); border-radius:10px; }}
  blockquote p {{ margin:6px 0; color:var(--muted); }}
  .table-wrap {{ overflow-x:auto; margin:20px 0; border:1px solid var(--line);
                 border-radius:14px; background:var(--panel); }}
  table {{ border-collapse:collapse; width:100%; min-width:640px; font-size:.9rem; }}
  th, td {{ padding:11px 14px; text-align:right; vertical-align:top;
            border-bottom:1px solid var(--line); }}
  th {{ background:rgba(110,168,254,.09); font-weight:700; white-space:nowrap; }}
  tr:last-child td {{ border-bottom:0; }}
  tbody tr:hover {{ background:rgba(110,168,254,.05); }}
  ul, ol {{ padding-right:24px; margin:12px 0; }}
  li {{ margin:7px 0; }}
  ul.check {{ list-style:none; padding-right:4px; }}
  .num {{ direction:ltr; unicode-bidi:isolate; white-space:nowrap; }}
  .toc {{ background:var(--panel); border:1px solid var(--line); border-radius:16px;
          padding:18px 22px; margin:28px 0 8px; }}
  .toc-title {{ font-size:.8rem; letter-spacing:.12em; color:var(--muted);
                text-transform:uppercase; margin-bottom:8px; }}
  .toc a {{ display:inline-block; margin:4px 0 4px 18px; font-size:.92rem; color:var(--ink); }}
  .toc a:hover {{ color:var(--accent); }}
  .lang {{ display:flex; gap:6px; justify-content:flex-end; margin-bottom:14px; }}
  .lang a {{ padding:5px 12px; border:1px solid var(--line); border-radius:999px;
             font-size:.82rem; color:var(--muted); }}
  .lang a.active {{ color:var(--ink); border-color:var(--accent);
                    background:rgba(110,168,254,.12); }}
  @media print {{
    body {{ background:#fff; color:#000; }}
    .lang {{ display:none; }}
    .toc {{ break-inside:avoid; }}
    h2 {{ break-after:avoid; }}
    .table-wrap {{ break-inside:avoid; }}
  }}
  {align_css}
</style>
</head>
<body>
<div class="wrap">
{nav}
{''.join(out)}
</div>
</body>
</html>"""

if toc:
    block = f'<nav class="toc"><div class="toc-title">{toc_label}</div>{toc_html}</nav>'
    idx = html_doc.find("<hr>")
    if idx != -1:
        html_doc = html_doc[:idx] + block + html_doc[idx:]

open(OUT, "w", encoding="utf-8").write(html_doc)
print("wrote", OUT, len(html_doc), "bytes,", len(toc), "toc items,", LANG)
