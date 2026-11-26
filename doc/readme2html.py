#!/usr/bin/env python3
# ManicTime Tracker for Thunderbird - Copyright (C) 2026 Jürgen Hörmann
# SPDX-License-Identifier: GPL-3.0-or-later
"""Converts Markdown files into the restricted HTML that addons.thunderbird.net
(AMO) accepts:
    README.md        -> doc/README.html   (add-on description)
    test/TESTING.md  -> doc/TESTING.html  (test instructions for reviewers)

    python3 doc/readme2html.py              # all of the above
    python3 doc/readme2html.py SRC.md DST.html

AMO allows only: <a href title> <abbr title> <acronym title> <b> <blockquote>
<code> <em> <i> <li> <ol> <strong> <ul>. No headings and no paragraphs, so:
- the H1 (the title, shown by AMO anyway) is dropped,
- other headings become <b>Heading</b>,
- paragraphs are separated by a blank line (AMO turns newlines into breaks),
- each list is written on a single line, so AMO adds no extra breaks in it,
- fenced code blocks become <code> (inside a list item: appended to it),
- relative links point to the file on GitHub.

Supported Markdown: headings, paragraphs, nested "-"/"*" and "1." lists
(any consistent indentation), ``` code blocks, > blockquotes, `code`, **bold**,
*italic*, [text](url), <https://autolink>.
"""
import html
import re
import sys
from pathlib import Path

REPO_URL = "https://github.com/jhit/ManicTime-Tracker-for-Thunderbird/blob/main/"
ROOT = Path(__file__).resolve().parent.parent
FILES = [("README.md", "doc/README.html"), ("test/TESTING.md", "doc/TESTING.html")]

base_url = REPO_URL  # GitHub URL of the source file's folder, for relative links


def inline(text):
    # Split off code spans first so their content is not formatted.
    out = []
    for i, part in enumerate(re.split(r"(`[^`]*`)", text)):
        if i % 2:
            out.append(code(part[1:-1]))
            continue
        links = []

        def keep(a):  # protect finished links from the formatting below
            links.append(a)
            return "\0%d\0" % (len(links) - 1)

        def link(m):
            url = m.group(2)
            if not re.match(r"[a-z][a-z0-9+.-]*:", url, re.I):
                url = base_url + re.sub(r"^\./", "", url)
            return keep('<a href="%s">%s</a>' % (html.escape(url), fmt(html.escape(m.group(1), quote=False))))

        s = re.sub(r"<(https?://[^>\s]+)>",
                   lambda m: keep('<a href="%s">%s</a>' % ((html.escape(m.group(1)),) * 2)), part)
        s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, s)
        s = fmt(html.escape(s, quote=False))
        s = re.sub(r"\0(\d+)\0", lambda m: links[int(m.group(1))], s)
        out.append(s)
    return "".join(out)


def fmt(s):
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)


def code(text):
    return "<code>" + html.escape(text, quote=False) + "</code>"


LIST_RE = re.compile(r"^( *)([-*]|\d+\.) +(.*)$")
FENCE_RE = re.compile(r"^ *```")


def read_fence(lines, i):
    """lines[i] opens a fence. Returns (html, index after the closing fence)."""
    indent = len(lines[i]) - len(lines[i].lstrip())
    body = []
    i += 1
    while i < len(lines) and not FENCE_RE.match(lines[i]):
        body.append(lines[i][indent:] if lines[i][:indent].strip() == "" else lines[i])
        i += 1
    return code("\n".join(body)), i + 1


def render_list(items):
    """items: list of (indent, ordered, html). Returns HTML on one line."""
    out = []
    stack = []  # (indent, tag)
    for indent, ordered, text in items:
        tag = "ol" if ordered else "ul"
        while stack and indent < stack[-1][0]:
            out.append("</li></%s>" % stack.pop()[1])
        if stack and indent == stack[-1][0]:
            out.append("</li>")
        else:
            stack.append((indent, tag))
            out.append("<%s>" % tag)
        out.append("<li>" + text)
    while stack:
        out.append("</li></%s>" % stack.pop()[1])
    return "".join(out)


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
        if FENCE_RE.match(line):
            block, i = read_fence(lines, i)
            blocks.append(block)
            continue
        if LIST_RE.match(line):
            items = []  # [indent, ordered, html]
            while i < len(lines) and lines[i].strip():
                m = LIST_RE.match(lines[i])
                if FENCE_RE.match(lines[i]) and items:
                    block, i = read_fence(lines, i)
                    items[-1][2] += " " + block
                    continue
                if m:
                    items.append([len(m.group(1)), m.group(2)[0].isdigit(), inline(m.group(3))])
                elif items:  # continuation line of the previous item
                    items[-1][2] += " " + inline(lines[i].strip())
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
               and not LIST_RE.match(lines[i]) and not lines[i].startswith(">")
               and not FENCE_RE.match(lines[i])):
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


def generate(src, dst):
    global base_url
    src, dst = ROOT / src, ROOT / dst
    folder = src.parent.relative_to(ROOT).as_posix()
    base_url = REPO_URL + ("" if folder == "." else folder + "/")
    dst.write_text(convert(src.read_text(encoding="utf-8")), encoding="utf-8")
    print("Created " + dst.relative_to(ROOT).as_posix())


def main():
    args = sys.argv[1:]
    if len(args) == 2:
        generate(Path(args[0]).resolve().relative_to(ROOT), Path(args[1]).resolve().relative_to(ROOT))
    elif not args:
        for src, dst in FILES:
            generate(src, dst)
    else:
        sys.exit("usage: readme2html.py [SRC.md DST.html]")


if __name__ == "__main__":
    main()
