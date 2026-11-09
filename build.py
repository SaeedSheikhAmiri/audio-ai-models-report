#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Minimal Markdown -> styled RTL HTML converter for the audio-AI report."""
import re, html, sys

SRC = sys.argv[1]
OUT = sys.argv[2]

text = open(SRC, encoding="utf-8").read()
lines = text.split("\n")

NUM_RE = re.compile(r"(\$[0-9۰-۹][0-9۰-۹.,٫/–\-]*|[0-9۰-۹][0-9۰-۹.,٫/–\-]*(?:ms|s|k|M|B)(?![A-Za-z۰-۹])|[0-9۰-۹]+(?:\.[0-9۰-۹]+)?%|[0-9۰-۹]+(?:×|x)[0-9۰-۹]+)")

def inline(s):
    s = html.escape(s, quote=False)
    s = NUM_RE.sub(lambda m: '<span class="num">' + m.group(0) + '</span>', s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s

def is_table_sep(line):
    return bool(re.match(r"^\s*\|[\s:\-|]+\|\s*$", line)) and "-" in line

def split_row(line):
    line = line.strip()
    if line.startswith("|"): line = line[1:]
    if line.endswith("|"): line = line[:-1]
    return [c.strip() for c in line.split("|")]

out = []
i = 0
toc = []
in_list = None   # 'ul' | 'ol'
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

    # code fence
    if stripped.startswith("```"):
        close_list(); close_quote()
        j = i + 1
        buf = []
        while j < len(lines) and not lines[j].strip().startswith("```"):
            buf.append(lines[j]); j += 1
        out.append("<pre><code>" + html.escape("\n".join(buf)) + "</code></pre>")
        i = j + 1
        continue

    # blank
    if not stripped:
        close_list(); close_quote()
        i += 1
        continue

    # heading
    m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
    if m:
        close_list(); close_quote()
        level = len(m.group(1))
        content = inline(m.group(2))
        if level == 2:
            anchor = "s" + str(len(toc) + 1)
            toc.append((anchor, m.group(2)))
            out.append(f'<h2 id="{anchor}">{content}</h2>')
        else:
            out.append(f"<h{level}>{content}</h{level}>")
        i += 1
        continue

    # hr
    if re.match(r"^(-{3,}|\*{3,})$", stripped):
        close_list(); close_quote()
        out.append("<hr>")
        i += 1
        continue

    # table
    if stripped.startswith("|") and i + 1 < len(lines) and is_table_sep(lines[i + 1]):
        close_list(); close_quote()
        headers = split_row(stripped)
        i += 2
        rows = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            rows.append(split_row(lines[i]))
            i += 1
        out.append("<div class='table-wrap'><table><thead><tr>")
        for h in headers:
            out.append(f"<th>{inline(h)}</th>")
        out.append("</tr></thead><tbody>")
        for r in rows:
            out.append("<tr>")
            for c in r:
                out.append(f"<td>{inline(c)}</td>")
            out.append("</tr>")
        out.append("</tbody></table></div>")
        continue

    # blockquote
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

    # checklist
    m = re.match(r"^-\s+\[( |x|X)\]\s+(.*)$", stripped)
    if m:
        if in_list != "ul":
            close_list(); out.append("<ul class='check'>"); in_list = "ul"
        mark = "☑" if m.group(1).lower() == "x" else "☐"
        out.append(f"<li>{mark} {inline(m.group(2))}</li>")
        i += 1
        continue

    # unordered list
    m = re.match(r"^[-*]\s+(.*)$", stripped)
    if m:
        if in_list != "ul":
            close_list(); out.append("<ul>"); in_list = "ul"
        out.append(f"<li>{inline(m.group(1))}</li>")
        i += 1
        continue

    # ordered list
    m = re.match(r"^(\d+)\.\s+(.*)$", stripped)
    if m:
        if in_list != "ol":
            close_list(); out.append("<ol>"); in_list = "ol"
        out.append(f"<li>{inline(m.group(2))}</li>")
        i += 1
        continue

    # paragraph
    close_list()
    out.append(f"<p>{inline(stripped)}</p>")
    i += 1

close_list(); close_quote()

toc_html = "".join(f'<a href="#{a}">{html.escape(t)}</a>' for a, t in toc)

html_doc = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>نقشهٔ جامع مدل‌های صوتی هوش مصنوعی</title>
<style>
  :root {{
    --bg:#0f1115; --panel:#161922; --ink:#e8eaf0; --muted:#9aa3b2;
    --line:#262b38; --accent:#6ea8fe; --accent2:#8ee6c8; --warn:#ffd479;
    --code:#1d2230;
  }}
  @media (prefers-color-scheme: light) {{
    :root {{ --bg:#fbfbfd; --panel:#fff; --ink:#1a1d24; --muted:#5b6472;
             --line:#e4e7ee; --accent:#2563eb; --accent2:#0f8a6a; --warn:#9a6700;
             --code:#f2f4f8; }}
  }}
  * {{ box-sizing:border-box; }}
  body {{
    margin:0; background:var(--bg); color:var(--ink);
    font-family:"Vazirmatn","IRANSans","SF Pro Text","Segoe UI",Tahoma,sans-serif;
    line-height:1.95; font-size:16px;
  }}
  .wrap {{ max-width:1080px; margin:0 auto; padding:48px 28px 96px; }}
  h1 {{ font-size:2.1rem; line-height:1.5; margin:0 0 6px; letter-spacing:-.5px; }}
  h2 {{ font-size:1.45rem; margin:56px 0 16px; padding-bottom:10px;
        border-bottom:1px solid var(--line); color:var(--ink); }}
  h3 {{ font-size:1.12rem; margin:32px 0 10px; color:var(--accent); }}
  h1 + h3 {{ color:var(--muted); font-weight:500; font-size:1.02rem; margin-top:0; }}
  p {{ margin:12px 0; }}
  a {{ color:var(--accent); text-decoration:none; border-bottom:1px solid transparent; }}
  a:hover {{ border-bottom-color:var(--accent); }}
  strong {{ color:var(--ink); }}
  .num {{ direction:ltr; unicode-bidi:isolate; white-space:nowrap; }}
  code {{ background:var(--code); padding:2px 6px; border-radius:6px;
          font-family:"SF Mono",ui-monospace,Menlo,monospace; font-size:.88em; direction:ltr;
          display:inline-block; }}
  pre {{ background:var(--code); padding:16px; border-radius:12px; overflow:auto; direction:ltr; text-align:left; }}
  pre code {{ background:none; padding:0; }}
  hr {{ border:0; border-top:1px solid var(--line); margin:40px 0; }}
  blockquote {{
    margin:22px 0; padding:16px 20px; background:var(--panel);
    border-right:3px solid var(--accent2); border-radius:10px; color:var(--ink);
  }}
  blockquote p {{ margin:6px 0; color:var(--muted); }}
  .table-wrap {{ overflow-x:auto; margin:20px 0; border:1px solid var(--line);
                 border-radius:14px; background:var(--panel); }}
  table {{ border-collapse:collapse; width:100%; min-width:640px; font-size:.9rem; }}
  th, td {{ padding:11px 14px; text-align:right; vertical-align:top;
            border-bottom:1px solid var(--line); }}
  th {{ background:rgba(110,168,254,.09); font-weight:700; white-space:nowrap;
        position:sticky; top:0; backdrop-filter:blur(8px); }}
  tr:last-child td {{ border-bottom:0; }}
  tbody tr:hover {{ background:rgba(110,168,254,.05); }}
  ul, ol {{ padding-right:24px; margin:12px 0; }}
  li {{ margin:7px 0; }}
  ul.check {{ list-style:none; padding-right:4px; }}
  ul.check li {{ color:var(--ink); }}
  .toc {{ background:var(--panel); border:1px solid var(--line); border-radius:16px;
          padding:18px 22px; margin:28px 0 8px; }}
  .toc-title {{ font-size:.8rem; letter-spacing:.12em; color:var(--muted);
                text-transform:uppercase; margin-bottom:8px; }}
  .toc a {{ display:inline-block; margin:4px 0 4px 18px; font-size:.92rem; color:var(--ink); }}
  .toc a:hover {{ color:var(--accent); }}
  .meta {{ color:var(--muted); font-size:.85rem; margin-bottom:26px; }}
  @media print {{
    body {{ background:#fff; color:#000; }}
    .toc {{ break-inside:avoid; }}
    h2 {{ break-after:avoid; }}
    .table-wrap {{ break-inside:avoid; }}
  }}
</style>
</head>
<body>
<div class="wrap">
<div class="meta">گزارش پژوهشی · تهیه‌شده در نوامبر ۲۰۲۶ · اعداد قیمت تقریبی و نیازمند تأیید</div>
{''.join(out)}
</div>
</body>
</html>"""

# inject TOC after the intro hr (first <hr>)
if toc:
    toc_block = f'<nav class="toc"><div class="toc-title">فهرست</div>{toc_html}</nav>'
    idx = html_doc.find("<hr>")
    if idx != -1:
        html_doc = html_doc[:idx] + toc_block + html_doc[idx:]

open(OUT, "w", encoding="utf-8").write(html_doc)
print("wrote", OUT, len(html_doc), "bytes,", len(toc), "toc items")
