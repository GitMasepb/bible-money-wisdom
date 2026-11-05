#!/usr/bin/env python3
"""Builds verses.js for the Bible & Money diagram.

Text comes ONLY from Crossway's official ESV API (https://api.esv.org).
Get a free key at https://api.esv.org/account/create-application/ then run:

    ESV_API_KEY=your_key python3 build_verses.py

Without a key (or with --refs-only) it writes references only, and the page
shows each reference with a link to read it on esv.org.
"""
import json, os, re, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
API = "https://api.esv.org/v3/passage/text/"
LIMIT = 500  # ESV permission: quote up to 500 verses without written permission


def verse_count(ref):
    m = re.search(r":(\d+)(?:-(\d+))?$", ref)
    return int(m.group(2) or m.group(1)) - int(m.group(1)) + 1 if m else 1


def fetch(ref, key):
    params = urllib.parse.urlencode({
        "q": ref, "include-passage-references": "false", "include-verse-numbers": "false",
        "include-first-verse-numbers": "false", "include-footnotes": "false",
        "include-footnote-body": "false", "include-headings": "false",
        "include-short-copyright": "false", "include-selahs": "false",
        "indent-paragraphs": "0", "indent-poetry": "false", "indent-declares": "0",
        "indent-psalm-doxology": "0", "line-length": "0",
    })
    req = urllib.request.Request(f"{API}?{params}", headers={"Authorization": f"Token {key}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    return re.sub(r"\s+", " ", " ".join(data["passages"])).strip()


def main():
    topics = json.load(open(os.path.join(HERE, "topics.json")))
    refs = sorted({r for t in topics for r in t["refs"]})
    total = sum(verse_count(r) for r in refs)
    print(f"{len(refs)} unique passages, ~{total} verses (limit {LIMIT})")
    if total > LIMIT:
        sys.exit("Over the ESV 500-verse quotation limit. Trim topics.json.")

    key = os.environ.get("ESV_API_KEY")
    texts = {}
    if key and "--refs-only" not in sys.argv:
        for i, ref in enumerate(refs, 1):
            texts[ref] = fetch(ref, key)
            print(f"[{i}/{len(refs)}] {ref}")
            time.sleep(1.1)  # stay under 60 requests/minute
    else:
        print("No ESV_API_KEY set: writing references only.")

    out = {"translation": "ESV", "topics": topics, "texts": texts}
    with open(os.path.join(HERE, "verses.js"), "w") as f:
        f.write("window.DATA = " + json.dumps(out, ensure_ascii=False, indent=1) + ";\n")
    print("Wrote verses.js")


if __name__ == "__main__":
    main()
