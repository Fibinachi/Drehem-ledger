#!/usr/bin/env python3
"""Pilot: attribute inflows via received-markers (mu-ku / i3-dab5 / szu ba-ti).

In Drehem receipt formulae the receiver is named adjacent to the marker:
    mu-ku(DU)
    ab-ba-sa6-ga
    i3-dab5
i.e. delivered -> Abbasaga -> seized. A bare name next to a received-marker
is the receiver. Direction per tablet:
  - 'ki X-ta' (+ no received-marker naming someone else) with X the hub -> outflow
  - received-marker + hub named adjacent (not in from-slot) -> inflow
"""
import re, csv, json
from collections import defaultdict
from mass_balance_pilot import (VAL, COMMOD, TITLES, NAME_PAT, clean, is_name,
                                base_comm)

RECV = ('mu-ku', 'i3-dab5', 'szu ba-ti')


def tablet_lines(text):
    out = []
    for raw in text.split('\n'):
        l = raw.strip()
        if not l or l[0] in '>@#&$':
            continue
        l = re.sub(r'^\d+\.\s*', '', l)
        if not l or l.startswith(('@', '&', '$', '>>', '#')):
            continue
        out.append(l)
    return out


def bare_names(line):
    """Personal names on a line that carry no slot marker."""
    found = []
    tmp = re.sub(r'\bki\s+', '', line)
    tmp = re.sub(r'-ta\b', '', tmp)
    tmp = re.sub(r'-še3\b', '', tmp)
    tmp = re.sub(r'\bgiri3\s+[a-z][a-z0-9\-\.šĝḫŋřž]+', '', tmp)
    tmp = re.sub(r'\bmaškim\s+[a-z][a-z0-9\-\.šĝḫŋřž]+', '', tmp)
    for tok in re.findall(r'[a-z][a-z0-9\-\.šĝḫŋřž]+', tmp):
        c = clean(tok)
        if is_name(c) and c not in TITLES:
            found.append(c)
    return found


def analyze(text):
    lines = tablet_lines(text)
    qtys = defaultdict(int)
    froms, tos = set(), set()
    recv_idx = []
    for i, l in enumerate(lines):
        for m in re.finditer(
                r'((?:\d+\([a-z0-9]+\)\s*)+)\s*([a-z][a-z0-9\-\.šĝḫŋřž]*)', l):
            comm = base_comm(m.group(2))
            if comm not in COMMOD:
                continue
            qty = sum(int(q.group(1)) * VAL.get(q.group(2), 0)
                      for q in re.finditer(r'(\d+)\(([a-z0-9]+)\)', m.group(1)))
            if qty:
                qtys[comm] += qty
        for pat in (r'\bki (%s)(?:-ta)?(?:\s|$)' % NAME_PAT,
                    r'\b(%s)-ta\b' % NAME_PAT):
            for mm in re.finditer(pat, l):
                c = re.sub(r'-ta$', '', clean(mm.group(1)))
                if is_name(c):
                    froms.add(c)
        for mm in re.finditer(r'\b(%s)-še3\b' % NAME_PAT, l):
            c = clean(mm.group(1))
            if is_name(c):
                tos.add(c)
        if any(r in l for r in RECV):
            recv_idx.append(i)
    # receiver = bare names on/adjacent to received-marker lines
    receivers = set()
    for i in recv_idx:
        for j in (i - 1, i, i + 1):
            if 0 <= j < len(lines):
                receivers.update(bare_names(lines[j]))
    # a from-slot name is not the receiver
    receivers -= froms
    return qtys, froms, tos, receivers, bool(recv_idx)


def main():
    dates = {}
    with open('sources/drehem_dates.csv') as f:
        for row in csv.DictReader(f):
            m = re.match(r'([^.]+)\.(\d+)\.', row['dates_referenced'] or '')
            dates[row['P']] = (m.group(1), int(m.group(2))) if m else (None, None)

    flows = defaultdict(lambda: {'in': 0, 'out': 0, 'n_in': 0, 'n_out': 0})
    n_recv = n_ab_in = n_ab_out = 0
    buf, cur = [], None
    with open('sources/drehem.atf', encoding='utf-8') as f:
        for line in f:
            if line.startswith('&P') and buf:
                qtys, froms, tos, receivers, has_recv = analyze(''.join(buf))
                king, year = dates.get(cur, (None, None))
                ab_from = any('ab-ba-sa6-ga' in x for x in froms)
                ab_recv = any('ab-ba-sa6-ga' in x for x in receivers)
                if has_recv:
                    n_recv += 1
                for comm, qty in qtys.items():
                    k = (comm, king, year)
                    if ab_from:
                        flows[k]['out'] += qty
                        flows[k]['n_out'] += 1
                        n_ab_out += 1
                    if ab_recv:
                        flows[k]['in'] += qty
                        flows[k]['n_in'] += 1
                        n_ab_in += 1
                buf, cur = [line], line[1:].split()[0]
            else:
                buf.append(line)

    print(f"tablets with received-markers: {n_recv}")
    print(f"abbasaga outflow txns: {n_ab_out}, inflow txns: {n_ab_in}")
    rows = sorted(
        ((c, k, y, v['in'], v['out'], v['in'] - v['out'], v['n_in'], v['n_out'])
         for (c, k, y), v in flows.items() if k == 'Amar-Suen' and (v['in'] or v['out'])),
        key=lambda r: (r[0], r[2]))
    print(f"\n{'comm':8} {'yr':>3} {'in':>10} {'out':>10} {'net':>10}")
    tot_in = tot_out = 0
    for c, k, y, i, o, net, ni, no in rows:
        if c == 'udu':
            print(f"{c:8} {y:>3} {i:>10,} {o:>10,} {net:>10,}")
            tot_in += i
            tot_out += o
    print(f"\nudu totals AS.1-9: in={tot_in:,} out={tot_out:,} net={tot_in-tot_out:,}")
    json.dump(
        [{'comm': c, 'king': k, 'year': y, 'in': i, 'out': o}
         for c, k, y, i, o, net, ni, no in rows],
        open('sources/abbasaga_balanced.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
