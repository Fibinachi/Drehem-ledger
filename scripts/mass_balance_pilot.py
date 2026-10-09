#!/usr/bin/env python3
"""Pilot: directional flows for Abbasaga (ab-ba-sa6-ga) per commodity per year.
Parses drehem.atf, extracts (commodity, qty, from, to) per tablet line,
joins catalog dates, aggregates inflows vs outflows for the hub official.
"""
import re, csv, json
from collections import defaultdict

VAL = {'disz': 1, 'u': 10, 'gesz2': 60, 'geszu': 600, 'szar2': 3600, 'szargal': 21600}
COMMOD = {'udu', 'gu4', 'masz2', 'sila4', 'ud5', 'kir11', 'u8',
          'dusu2-nita2', 'dusu2-munus', 'anszu', 'ab2', 'amar',
          'gukkal', 'masz-da3', 'dara4', 'szeg9-bar', 'lulim', 'uz'}
TITLES = {'dub-sar', 'sipa', 'ugula', 'ensi2', 'szabra', 'sagi', 'nu-banda3',
          'kuruszda', 'ma2-lah5', 'nargal'}

NAME_PAT = r'[a-z][a-z0-9\-\.šĝḫŋřž]*'


def clean(tok):
    t = re.sub(r'\{[a-z]+\}', '', tok).strip('-.')
    return t


def is_name(tok):
    t = clean(tok)
    if len(t) < 4 or t in TITLES:
        return False
    if t[0].isdigit() or '(' in t or ')' in t:
        return False
    return bool(re.match(r'^[a-z]', t))


def names_in(pattern, line):
    out = []
    for m in re.finditer(pattern, line):
        c = clean(m.group(1))
        if is_name(c):
            out.append(c)
    return out


ADJ = {'gal', 'tur', 'mah', 'nita2', 'munus', 'sag', 'us2'}


def base_comm(tok):
    """Strip adjective suffixes: masz2-gal -> masz2."""
    t = clean(tok)
    parts = t.split('-')
    while len(parts) > 1 and parts[-1] in ADJ:
        parts.pop()
    return '-'.join(parts)


def parse_tablet(text):
    """Tablet-level: collect all (commodity, qty) and all from/to parties,
    then associate. Yields (commodity, total_qty, froms, tos)."""
    qtys = defaultdict(int)
    froms, tos = set(), set()
    for raw in text.split('\n'):
        l = raw.strip()
        if not l or l[0] in '>@#&$':
            continue
        l = re.sub(r'^\d+\.\s*', '', l)
        if not l or l.startswith(('@', '&', '$', '>>', '#')):
            continue
        for m in re.finditer(
                r'((?:\d+\([a-z0-9]+\)\s*)+)\s*([a-z][a-z0-9\-\.šĝḫŋřž]*)', l):
            qstr, comm = m.group(1), base_comm(m.group(2))
            if comm not in COMMOD:
                continue
            qty = sum(int(q.group(1)) * VAL.get(q.group(2), 0)
                      for q in re.finditer(r'(\d+)\(([a-z0-9]+)\)', qstr))
            if qty > 0:
                qtys[comm] += qty
        for pat in (r'\bki (%s)(?:-ta)?(?:\s|$)' % NAME_PAT,
                    r'\b(%s)-ta\b' % NAME_PAT):
            for mm in re.finditer(pat, l):
                c = clean(mm.group(1))
                # strip a trailing -ta the greedy ki-pattern may have eaten
                c = re.sub(r'-ta$', '', c)
                if is_name(c):
                    froms.add(c)
        for mm in re.finditer(r'\b(%s)-še3\b' % NAME_PAT, l):
            c = clean(mm.group(1))
            if is_name(c):
                tos.add(c)
    for comm, qty in qtys.items():
        if froms or tos:
            yield comm, qty, sorted(froms), sorted(tos)


def main():
    dates = {}
    with open('sources/drehem_dates.csv') as f:
        for row in csv.DictReader(f):
            m = re.match(r'([^.]+)\.(\d+)\.', row['dates_referenced'] or '')
            dates[row['P']] = (m.group(1), int(m.group(2))) if m else (None, None)

    flows = defaultdict(lambda: {'in': 0, 'out': 0, 'n': 0})
    n_ab, buf, cur = 0, [], None
    with open('sources/drehem.atf', encoding='utf-8') as f:
        for line in f:
            if line.startswith('&P') and buf:
                king, year = dates.get(cur, (None, None))
                for comm, qty, froms, tos in parse_tablet(''.join(buf)):
                    ab_from = any('ab-ba-sa6-ga' in x for x in froms)
                    ab_to = any('ab-ba-sa6-ga' in x for x in tos)
                    if ab_from or ab_to:
                        n_ab += 1
                        k = (comm, king, year)
                        if ab_from:
                            flows[k]['out'] += qty
                        if ab_to:
                            flows[k]['in'] += qty
                        flows[k]['n'] += 1
                buf, cur = [line], line[1:].split()[0]
            else:
                buf.append(line)

    print(f"abbasaga directional txns: {n_ab}")
    rows = sorted(
        ((c, k, y, v['in'], v['out'], v['in'] - v['out'], v['n'])
         for (c, k, y), v in flows.items() if k == 'Amar-Suen'),
        key=lambda r: (r[0], r[2]))
    print(f"\n{'comm':8} {'yr':>3} {'in':>10} {'out':>10} {'net':>10} {'n':>5}")
    for c, k, y, i, o, net, nn in rows:
        print(f"{c:8} {y:>3} {i:>10,} {o:>10,} {net:>10,} {nn:>5}")
    json.dump(
        [{'comm': c, 'king': k, 'year': y, 'in': i, 'out': o, 'n': nn}
         for c, k, y, i, o, net, nn in rows],
        open('sources/abbasaga_flows.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
