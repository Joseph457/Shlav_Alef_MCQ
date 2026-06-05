#!/usr/bin/env python3
"""Append-only merge of new question-bank items into questions.json.

Usage:
    python3 parse_bank.py questions.json "Question Bank - Sabiston.md" [more banks...]

Reads each bank markdown, parses every MCQ (question block + answer block), and
ADDS any item whose id is not already present in questions.json. Existing items are
preserved byte-for-byte. Aborts loudly if a bank looks truncated or any new item is
malformed -- this is the safety net against the OneDrive/bash truncation gotcha
(a stale bash read silently drops the '# ANSWER KEY' section and under-counts).
"""
import json, re, sys, os

SCHEMA = ['id','chapter','section','stem','options','answer','exp','hy','src','book','vol','chnum','chname']

def book_from_filename(path):
    b = os.path.basename(path)
    m = re.search(r'Question Bank - (.+)\.md$', b)
    return m.group(1).strip() if m else "Unknown"

def parse_bank(path):
    txt = open(path, encoding="utf-8", errors="ignore").read()
    book = book_from_filename(path)
    idx = txt.find("# ANSWER KEY")
    if idx == -1:
        sys.exit(f"ABORT: '{path}' has no '# ANSWER KEY' section -- almost certainly a "
                 f"truncated/stale read (OneDrive sync lag). Do NOT push. See CLAUDE.md gotcha.")
    qpart, apart = txt[:idx], txt[idx:]

    # chapter-name map from "## Chapter <n> — <name>" headings (strip trailing "(Vol ...)" )
    chname = {}
    for m in re.finditer(r'^##\s*Chapter\s+(\d+)\s*[—\-]\s*(.+?)\s*$', qpart, re.M):
        chname[m.group(1)] = re.sub(r'\s*\(Vol[^)]*\)\s*$', '', m.group(2)).strip()

    items = {}
    # optional markdown image line between stem and options: ![caption](images/<id>.jpg)
    qre = re.compile(r'^\*\*([A-Za-z0-9.\-]+)\*\*\s*\*\[(.*?)\]\*\s*(.*?)\n(?:!\[([^\]]*)\]\(\s*([^)\s]+)\s*\)\s*\n)?((?:- [A-D]\..*\n?)+)', re.M)
    for m in qre.finditer(qpart):
        qid, tag, stem, imgcap, imgpath, opts = m.groups()
        cm = re.match(r'Ch\s*(\d+)\s*·\s*(.*)', tag)
        chnum = cm.group(1) if cm else ""
        section = (cm.group(2).strip() if cm else tag.strip())
        options = {o.group(1): o.group(2).strip() for o in re.finditer(r'- ([A-D])\.\s*(.*)', opts)}
        vol = ""
        vm = re.match(r'[A-Z]-([IVX]+)-', qid)
        if vm: vol = vm.group(1)
        it = {'id':qid,'chapter':'Ch'+chnum,'section':section,'stem':stem.strip(),
                      'options':options,'book':book,'vol':vol,'chnum':chnum,
                      'chname':chname.get(chnum,'')}
        if imgpath:
            it['image'] = imgpath.strip()
            if imgcap and imgcap.strip(): it['imgcap'] = imgcap.strip()
        items[qid] = it

    are = re.compile(r'^\*\*([A-Za-z0-9.\-]+)\s*[—\-]\s*([A-D])\.\*\*\s*(.*?)\s*🔑\s*(.*?)\s*📖\s*(.*?)\s*$', re.M)
    for m in are.finditer(apart):
        qid, ans, exp, hy, src = m.groups()
        if qid in items:
            items[qid]['answer'] = ans
            items[qid]['exp'] = exp.strip()
            items[qid]['hy'] = hy.strip()
            items[qid]['src'] = re.sub(r'\s*\[[a-z]+\]\s*$', '', src).strip()
    # per-option `- why X:` lines (workflow B2): associate to the most-recent answer id
    cur = None
    aline = re.compile(r'^\*\*([A-Za-z0-9.\-]+)\s*[—\-]\s*[A-D]\.\*\*')
    wline = re.compile(r'^\s*-\s*why\s+([A-D])\s*:\s*(.*\S)\s*$')
    for line in apart.splitlines():
        am = aline.match(line)
        if am:
            cur = am.group(1); continue
        wm = wline.match(line)
        if wm and cur in items:
            items[cur].setdefault('why', {})[wm.group(1)] = wm.group(2).strip()
    return items

def main():
    if len(sys.argv) < 3:
        sys.exit("usage: parse_bank.py questions.json <bank.md> [bank.md ...]")
    qjson, banks = sys.argv[1], sys.argv[2:]
    existing = json.load(open(qjson, encoding="utf-8"))
    have = {x['id'] for x in existing}

    new = []
    for bank in banks:
        items = parse_bank(bank)
        for qid, it in items.items():
            if qid in have:
                continue
            # vol is legitimately empty for non-Neligan books (Sabiston/Bologna have no volume)
            required = [k for k in SCHEMA if k != 'vol']
            missing = [k for k in required if k not in it or it[k] in (None, "", {})]
            if 'options' in it and len(it['options']) == 4 and all(it['options'].get(k) for k in "ABCD"):
                missing = [k for k in missing if k != 'options']
            if missing:
                sys.exit(f"ABORT: new item {qid} is incomplete (missing/empty {missing}) -- "
                         f"likely a truncated bank read. Do NOT push.")
            rec = {k: it[k] for k in SCHEMA}
            for opt in ('image','imgcap','why'):
                if it.get(opt): rec[opt] = it[opt]
            new.append(rec)
            have.add(qid)

    merged = existing + new
    assert len({x['id'] for x in merged}) == len(merged), "duplicate ids after merge"
    json.dump(merged, open(qjson, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"added {len(new)} new items; total {len(merged)}")
    if new:
        from collections import Counter
        c = Counter((x['book'], x['chapter']) for x in new)
        for k in sorted(c): print(f"  +{c[k]}  {k[0]} {k[1]}")

if __name__ == "__main__":
    main()
