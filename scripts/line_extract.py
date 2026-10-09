#!/usr/bin/env python3
"""Phase 2a: line-level extractor.

Each ATF content line -> {quantities: [(commodity, qty)], froms, tos, vias,
markers, recipients}. No cross-line inference here; the clause assembler
(in phase 2b) resolves references between lines.
"""
import re
import sys
sys.path.insert(0, 'scripts')
from mass_balance_pilot import VAL, COMMOD, NAME_PAT, clean, is_name, base_comm

COMMOD_TOK = {'udu', 'gu4', 'masz2', 'masz', 'sila4', 'ud5', 'kir11', 'u8',
              'amar', 'ab2', 'sze', 'ga', 'i3', 'sila3', 'sza3-bi'}
# number-words and divine names are never persons
NONPERSON = {'gesz2', 'gesz', 'szar2', 'szar', 'limmu', 'nanna', 'en-lil2',
             'inanna', 'utu', 'szara2', 'nin-urta', 'en-ki', 'da-gan',
             'iszkur', 'nin-gal', 'nin-sun2', 'nin-a-zu', 'mes-lam',
             'dumu-zi', 'gesztin-an-na'}
RECV_MARKERS = ('mu-ku', 'i3-dab5', 'szu ba-ti', 'ba-zi', 'zi-ga')


def is_person(c):
    """Name-like token that isn't a commodity, number-word, or god."""
    import re as _re
    d = _re.sub(r'[0-9]', '', c)
    return is_name(c) and c not in COMMOD_TOK and d not in NONPERSON \
        and len(c) >= 4


def strip_struct(raw):
    """Remove ATF structural markup, return (line_no, text) or None."""
    l = raw.strip()
    if not l or l[0] in '>@#&$':
        return None
    m = re.match(r'(\d+)\.\s*(.*)$', l)
    if not m:
        return None
    text = m.group(2).strip()
    if not text or text.startswith(('@', '&', '$', '>>', '#')):
        return None
    return int(m.group(1)), text


def extract_line(text):
    """Extract everything on a single content line."""
    out = {'qty': [], 'from': set(), 'to': set(), 'via': set(),
           'markers': set(), 'names': set()}
    t = re.sub(r'\{(d|ki)\}', '', text)
    comm_tokens = set()
    # quantities: (n(g) ...) commodity
    for m in re.finditer(
            r'((?:\d+\([a-z0-9]+\)\s*)+)\s*([a-z][a-z0-9\-\.šĝḫŋřž]*)', t):
        comm = base_comm(m.group(2))
        if comm not in COMMOD:
            continue
        comm_tokens.add(m.group(2).strip())
        comm_tokens.add(comm)
        qty = sum(int(q.group(1)) * VAL.get(q.group(2), 0)
                  for q in re.finditer(r'(\d+)\(([a-z0-9]+)\)', m.group(1)))
        if qty:
            out['qty'].append((comm, qty))
    # from: ki X(-ta), X-ta
    for pat in (r'\bki (%s)(?:-ta)?(?:\s|$)' % NAME_PAT,
                r'\b(%s)-ta\b' % NAME_PAT):
        for m in re.finditer(pat, t):
            c = re.sub(r'-ta$', '', clean(m.group(1)))
            if is_person(c):
                out['from'].add(c)
    # to: X-še3
    for m in re.finditer(r'\b(%s)-še3\b' % NAME_PAT, t):
        c = clean(m.group(1))
        if is_person(c):
            out['to'].add(c)
    # via: giri3 X ; maškim X
    for pat in (r'\bgiri3 (%s)' % NAME_PAT, r'\bmaškim (%s)' % NAME_PAT):
        for m in re.finditer(pat, t):
            c = clean(m.group(1))
            if is_person(c):
                out['via'].add(c)
    # markers (damage-tolerant: szu# ba-ti)
    t_nodmg = re.sub(r'#', '', t)
    for mk in RECV_MARKERS:
        if mk in t_nodmg:
            out['markers'].add(mk)
    # bare names (candidate parties, filtered later)
    tmp = re.sub(r'\bki\s+', '', t)
    tmp = re.sub(r'-(ta|še3)\b', '', tmp)
    tmp = re.sub(r'\b(giri3|maškim)\s+[a-z][a-z0-9\-\.šĝḫŋřž]+', '', tmp)
    for tok in re.findall(r'[a-z][a-z0-9\-\.šĝḫŋřž]+', tmp):
        c = clean(tok)
        if (is_person(c) and c not in comm_tokens and len(c) >= 5
                and c not in out['from'] and c not in out['to']
                and c not in out['via']):
            out['names'].add(c)
    return out


def extract_tablet(text):
    """Full tablet -> list of (line_no, line_extract)."""
    lines = []
    for raw in text.split('\n'):
        s = strip_struct(raw)
        if s:
            no, t = s
            lines.append((no, t, extract_line(t)))
    return lines


if __name__ == '__main__':
    # demo on P100232 (the multi-delivery tablet)
    buf = []
    with open('sources/drehem.atf', encoding='utf-8') as f:
        for line in f:
            if line.startswith('&P100232 ') and buf or \
               (line.startswith('&P') and buf and buf[0].startswith('&P100232 ')):
                break
            if line.startswith('&P100232 '):
                buf = [line]
            elif buf and line.startswith('&P'):
                break
            elif buf:
                buf.append(line)
    for no, t, e in extract_tablet(''.join(buf)):
        print(f"{no:2d} | {t[:55]:55s} | qty={e['qty']} from={sorted(e['from'])} "
              f"mk={sorted(e['markers'])} names={sorted(e['names'])[:3]}")
