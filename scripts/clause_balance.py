#!/usr/bin/env python3
"""Phase 2c: corpus-wide clause assembly + recomputed flows.

Direction (tablet-level, symmetric like the validated naive version):
  - tablet has mu-ku/i3-dab5/szu ba-ti -> clauses are INFLOW
  - tablet has ba-zi/zi-ga, or from-parties without recv markers -> OUTFLOW
Quantities are now per-clause (the Phase 2 improvement).
"""
import re, csv, json
from collections import defaultdict, Counter
import sys
sys.path.insert(0, 'scripts')
from clause_assemble import assemble
from line_extract import RECV_MARKERS

OUT_MARKERS = ('ba-zi', 'zi-ga')


def load_officials():
    """Officials = Hilgert-validated + high-frequency from-names (desubscripted)."""
    import json
    roster = set()
    try:
        for n in json.load(open('sources/hilgert_roster_all.json')):
            roster.add(re.sub(r'[0-9]', '', n))
    except FileNotFoundError:
        pass
    freq = Counter()
    with open('sources/drehem.atf', encoding='utf-8') as f:
        for line in f:
            if line.startswith('&P'):
                continue
    # freq from precomputed file
    try:
        for n, c in json.load(open('sources/from_freq.json')).items():
            if c >= 50:
                roster.add(re.sub(r'[0-9]', '', n))
    except FileNotFoundError:
        pass
    roster.add('ab-ba-sa6-ga')
    return roster


def clause_direction(c, recv, outm, officials):
    """Institutional boundary = all officials (Hilgert roster + freq>=50).
    IN: external -> official. OUT: official -> external.
    TRANSFER: official -> official. None: unclear."""
    frm = {re.sub(r'[0-9]', '', x) for x in c['from']}
    to = {re.sub(r'[0-9]', '', x) for x in c['to']}
    # Abbasaga always counts as official (central office head)
    frm_off = {x for x in frm if x in officials or 'ab-ba-sa-ga' in x}
    to_off = {x for x in to if x in officials or 'ab-ba-sa-ga' in x}
    frm_ext = frm - frm_off - to_off  # not official on either side
    to_ext = to - to_off - frm_off
    # divine recipients are external (temples)
    if outm:
        return 'out'
    if frm_off and to_ext:
        return 'out'
    if frm_off and not to:
        return 'out'
    if frm_ext and to_off:
        return 'in'
    if not frm and to_off and recv:
        return 'in'
    if frm_off and to_off:
        return 'transfer'
    if recv and not frm_off:
        return 'in'
    return None


def tablet_markers(text):
    t = re.sub(r'\{(d|ki)\}', '', text)
    recv = any(m in t for m in RECV_MARKERS)
    out = any(m in t for m in OUT_MARKERS)
    return recv, out


def main():
    dates = {}
    with open('sources/drehem_dates.csv') as f:
        for row in csv.DictReader(f):
            m = re.match(r'([^.]+)\.(\d+)\.', row['dates_referenced'] or '')
            if m:
                dates[row['P']] = (m.group(1), int(m.group(2)))
    redated = json.load(open('sources/redated.json'))
    for pn, r in redated.items():
        k, y = r['date'].split('.')
        dates[pn] = (k, int(y))

    n_clauses = 0
    n_tablets = 0
    n_undirected = 0
    n_transfer = 0
    ab_in = ab_out = 0
    ab_clauses_in = ab_clauses_out = 0
    officials = load_officials()
    bal = defaultdict(lambda: {'in': 0, 'out': 0})
    conf_c = Counter()
    buf, cur = [], None
    with open('sources/drehem.atf', encoding='utf-8') as f:
        for line in f:
            if line.startswith('&P') and buf:
                t = ''.join(buf)
                clauses = assemble(t)
                if clauses:
                    n_tablets += 1
                    n_clauses += len(clauses)
                    recv, outm = tablet_markers(t)
                    king, year = dates.get(cur, (None, None))
                    for c in clauses:
                        conf_c[c['conf']] += 1
                        d = clause_direction(c, recv, outm, officials)
                        if d is None:
                            n_undirected += 1
                            continue
                        if d == 'transfer':
                            n_transfer += 1
                            continue
                        is_ab_from = any('ab-ba-sa6-ga' in x for x in c['from'])
                        is_ab_to = any('ab-ba-sa6-ga' in x for x in c['to'])
                        if d == 'in':
                            if king == 'Amar-Suen' and c['commodity'] == 'udu':
                                bal[year]['in'] += c['qty']
                            if is_ab_to:
                                ab_in += c['qty']
                                ab_clauses_in += 1
                        else:
                            if king == 'Amar-Suen' and c['commodity'] == 'udu':
                                bal[year]['out'] += c['qty']
                            if is_ab_from:
                                ab_out += c['qty']
                                ab_clauses_out += 1
                buf, cur = [line], line[1:].split()[0]
            else:
                buf.append(line)

    print(f"tablets with clauses: {n_tablets}, total clauses: {n_clauses} "
          f"({n_clauses/max(n_tablets,1):.2f}/tablet), undirected: {n_undirected}, "
          f"transfer: {n_transfer}")
    print(f"confidence: {dict(conf_c)}")
    print(f"\nAbbasaga clause-level: IN {ab_clauses_in} clauses / {ab_in:,} sheep; "
          f"OUT {ab_clauses_out} clauses / {ab_out:,} sheep")
    print(f"(tablet-level was: 833 in-txns / 20,380 in; 5,230 out-txns / 101,112 out)")
    print(f"\nInstitutional udu balance, Amar-Suen (clause-level):")
    print(f"{'yr':>3} {'in':>10} {'out':>10} {'net':>10}")
    ti = to = 0
    for y in range(1, 10):
        v = bal[y]
        net = v['in'] - v['out']
        print(f"{y:>3} {v['in']:>10,} {v['out']:>10,} {net:>10,}")
        ti += v['in']
        to += v['out']
    print(f"\nTOTAL: in={ti:,} out={to:,} net={ti-to:,} "
          f"({(ti-to)/max(to,1)*100:+.1f}%)")
    print("(tablet-level was: in=182,586 out=191,759 net=-9,173, -4.8%)")


if __name__ == '__main__':
    main()
