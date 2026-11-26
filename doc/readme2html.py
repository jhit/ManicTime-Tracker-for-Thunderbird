#!/usr/bin/env python3
# ManicTime Tracker for Thunderbird - Copyright (C) 2026 Jürgen Hörmann
# SPDX-License-Identifier: GPL-3.0-or-later
"""Converts README.md into doc/README.html, the template for the add-on
description on addons.thunderbird.net (AMO).

AMO allows only: <a href title> <abbr title> <acronym title> <b> <blockquote>
<code> <em> <i> <li> <ol> <strong> <ul>. No headings and no paragraphs, so:
- the H1 (add-on name, shown by AMO anyway) is dropped,
- other headings become <b>Heading</b>,
- paragraphs are separated by a blank line (AMO turns newlines into breaks),
- each list is written on a single line, so AMO adds no extra breaks in it,
- relative links point to the file on GitHub.

Supported Markdown: headings, paragraphs, nested "-"/"*" and "1." lists
(2 spaces per level), > blockquotes, `code`, **bold**, *italic*, [text](url).
"""
import html
import re
import sys
from pathlib import Path

REPO_URL = "https://github.com/jhit/ManicTime-Tracker-for-Thunderbird/blob/main/"
ROOT = Path(__file__).resolve().parent.parent


def inline(text):
    # Split off code spans first so their content is not formatted.
    out = []
    for i, part in enumerate(re.split(r"(`[^`]*`)", text)):
        if i % 2:
            out.append("<code>" + html.escape(part[1:-1], quote=False) + "</code>")
            continue
        s = html.escape(part, quote=False)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)

        def link(m):
            url = m.group(2)
            if not re.match(r"[a-z][a-z0-9+.-]*:", url, re.I):
                url = REPO_URL + url.lstrip("./")
            return '<a href="%s">%s</a>' % (html.escape(url), m.group(1))

        s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, s)
        out.append(s)
    return "".join(out)


LIST_RE = re.compile(r"^( *)([-*]|\d+\.) +(.*)$")


def render_list(lines):
    """lines: list of (indent, ordered, text). Returns HTML on one line."""
    html_out = []
    stack = []  # (indent, tag)
    for indent, ordered, text in lines:
        tag = "ol" if ordered else "ul"
        while stack and indent < stack[-1][0]:
            html_out.append("</li></%s>" % stack.pop()[1])
        if stack and indent == stack[-1][0]:
            html_out.append("</li>")
        else:
            stack.append((indent, tag))
            html_out.append("<%s>" % tag)
        html_out.append("<li>" + inline(text))
    while stack:
        html_out.append("</li></%s>" % stack.pop()[1])
    return "".join(html_out)


def convert(md):
    blocks = []
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        h = re.match(r"^(#+) +(.*)$", line)
        if h:
            if len(h.group(1)) > 1:
                blocks.append("<b>" + inline(h.group(2)) + "</b>")
            i += 1
            continue
        if LIST_RE.match(line):
            items = []
            while i < len(lines) and lines[i].strip():
                m = LIST_RE.match(lines[i])
                if m:
                    items.append((len(m.group(1)), m.group(2)[0].isdigit(), m.group(3)))
                elif items:  # continuation line of the previous item
                    ind, o, t = items[-1]
                    items[-1] = (ind, o, t + " " + lines[i].strip())
                i += 1
            blocks.append(render_list(items))
            continue
        if line.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i].lstrip(">").strip())
                i += 1
            blocks.append("<blockquote>" + inline(" ".join(quote)) + "</blockquote>")
            continue
        para = []
        while (i < len(lines) and lines[i].strip() and not re.match(r"^#+ ", lines[i])
               and not LIST_RE.match(lines[i]) and not lines[i].startswith(">")):
            para.append(lines[i].strip())
            i += 1
        blocks.append(inline(" ".join(para)))
    # A heading is followed directly by its content, blocks by a blank line.
    out = ""
    for b in blocks:
        if out:
            out += "\n" if out.endswith("</b>") else "\n\n"
        out += b
    return out + "\n"


def main():
    src = ROOT / "README.md"
    dst = ROOT / "doc" / "README.html"
    dst.write_text(convert(src.read_text(encoding="utf-8")), encoding="utf-8")
    print("Created " + str(dst.relative_to(ROOT)))


if __name__ == "__main__":
    sys.exit(main())
