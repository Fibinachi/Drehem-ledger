#!/usr/bin/env python3
"""Entity resolution pilot: classify parties as INTERNAL (Drehem administration)
vs EXTERNAL, then recompute the institutional balance with corrected direction.

Internal signature: high attestation count + appears in from/via/seal roles
(the administration's side of the tablet) + spans multiple years +
co-occurs with the Abbasaga hub.

Direction rules per tablet (quantities q, froms F, tos T, receivers R):
  - F internal, (T|R) external  -> OUTFLOW (disbursement)
  - F external, (R|T) internal or R empty (implicit institutional receipt) -> INFLOW
  - both internal               -> INTERNAL TRANSFER (tracked separately)
  - otherwise                   -> UNCLASSIFIED
"""
import re, csv, json
from collections import defaultdict, Counter
import sys
sys.path.insert(0, 'scripts')
from mass_balance_pilot import VAL, COMMOD, TITLES, NAME_PAT, clean, is_name, base_comm
from inflow_pilot import tablet_lines, bare_names, RECV


def extract_all(text):
    qtys = defaultdict(int)
    froms, tos, vias, seals = set(), set(), set(), set()
    recv = False
    in_seal = False
    for raw in text.split('\n'):
        l = raw.strip()
        if l.startswith('@seal'):
            in_seal = True
            continue
        if l.startswith('@'):
            in_seal = False
        if not l or l[0] in '>@#&$':
            continue
        l = re.sub(r'^\d+\.\s*', '', l)
        if not l or l.startswith(('@', '&', '$', '>>', '#')):
            continue
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
                    (seals if in_seal else froms).add(c)
        for mm in re.finditer(r'\b(%s)-še3\b' % NAME_PAT, l):
            c = clean(mm.group(1))
            if is_name(c):
                tos.add(c)
        for mm in re.finditer(r'\bgiri3 (%s)' % NAME_PAT, l):
            c = clean(mm.group(1))
            if is_name(c):
                vias.add(c)
        if any(r in l for r in RECV):
            recv = True
    receivers = set()
    lines = tablet_lines(text)
    for i, l in enumerate(lines):
        if any(r in l for r in RECV):
            for j in (i - 1, i, i + 1):
                if 0 <= j < len(lines):
                    receivers.update(n for n in bare_names(lines[j])
                                     if n not in TITLES)
    receivers -= froms
    return qtys, froms, tos, vias, seals, receivers, recv


def main():
    dates = {}
    with open('sources/drehem_dates.csv') as f:
        for row in csv.DictReader(f):
            m = re.match(r'([^.]+)\.(\d+)\.', row['dates_referenced'] or '')
            dates[row['P']] = (m.group(1), int(m.group(2))) if m else (None, None)

    # Pass 1: name statistics
    stats = defaultdict(lambda: Counter())
    years = defaultdict(set)
    co_ab = Counter()
    tablets = []
    buf, cur = [], None
    with open('sources/drehem.atf', encoding='utf-8') as f:
        for line in f:
            if line.startswith('&P') and buf:
                t = ''.join(buf)
                qtys, froms, tos, vias, seals, receivers, recv = extract_all(t)
                king, year = dates.get(cur, (None, None))
                tablets.append((cur, king, year, qtys, froms, tos, vias, seals, receivers, recv))
                alln = froms | tos | vias | seals | receivers
                for n in froms: stats[n]['from'] += 1
                for n in tos: stats[n]['to'] += 1
                for n in vias: stats[n]['via'] += 1
                for n in seals: stats[n]['seal'] += 1
                for n in receivers: stats[n]['recv'] += 1
                if year:
                    for n in alln:
                        years[n].add((king, year))
                if any('ab-ba-sa6-ga' in x for x in alln):
                    for n in alln:
                        if 'ab-ba-sa6-ga' not in n:
                            co_ab[n] += 1
                buf, cur = [line], line[1:].split()[0]
            else:
                buf.append(line)

    # Classify: internal = hub-connected frequent administrators
    internal = {'ab-ba-sa6-ga'}
    for n, c in stats.items():
        total = sum(c.values())
        admin_roles = c['from'] + c['via'] + c['seal']
        if total >= 15 and admin_roles >= 8 and len(years[n]) >= 3:
            internal.add(n)
    # add top Abbasaga co-occurrers not yet caught
    for n, cnt in co_ab.most_common(60):
        if cnt >= 8 and sum(stats[n].values()) >= 10:
            internal.add(n)

    print(f"distinct names: {len(stats)}")
    print(f"classified INTERNAL: {len(internal)}")
    print("sample internal:", sorted(internal)[:25])

    # Pass 2: corrected institutional balance (sheep, Amar-Suen)
    bal = defaultdict(lambda: {'in': 0, 'out': 0, 'xfer': 0, 'uncl': 0})
    for cur, king, year, qtys, froms, tos, vias, seals, receivers, recv in tablets:
        if king != 'Amar-Suen' or not year:
            continue
        f_int = {x for x in froms if x in internal}
        f_ext = froms - internal
        r_all = receivers | tos
        r_int = {x for x in r_all if x in internal}
        r_ext = r_all - internal
        for comm, qty in qtys.items():
            if comm != 'udu':
                continue
            k = year
            if f_int and r_ext:
                bal[k]['out'] += qty
            elif f_ext and (r_int or (recv and not r_all)):
                bal[k]['in'] += qty
            elif f_int and r_int:
                bal[k]['xfer'] += qty
            elif recv and not froms:
                bal[k]['in'] += qty  # implicit institutional receipt
            else:
                bal[k]['uncl'] += qty

    print(f"\n{'yr':>3} {'in':>10} {'out':>10} {'xfer':>10} {'uncl':>10} {'net':>10}")
    ti = to = tx = tu = 0
    for y in range(1, 10):
        v = bal[y]
        net = v['in'] - v['out']
        print(f"{y:>3} {v['in']:>10,} {v['out']:>10,} {v['xfer']:>10,} {v['uncl']:>10,} {net:>10,}")
        ti += v['in']; to += v['out']; tx += v['xfer']; tu += v['uncl']
    print(f"\nTOTAL: in={ti:,} out={to:,} xfer={tx:,} uncl={tu:,} net={ti-to:,}")
    json.dump({'internal': sorted(internal),
               'balance': {str(y): bal[y] for y in range(1, 10)}},
              open('sources/entity_balance.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
