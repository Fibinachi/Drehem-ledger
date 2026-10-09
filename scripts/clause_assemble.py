#!/usr/bin/env python3
"""Phase 2b: clause assembler.

State machine over a tablet's lines:
  - date lines (iti/mu) are skipped for transactions
  - 'ki X-ta' / 'X-ta' sets current_from
  - 'X-še3' sets current_to
  - the mu-ku / NAME / i3-dab5 sequence sets tablet_recipient
  - a quantity line emits one clause per (commodity, qty):
      from = line.from or line bare-names or current_from
      to   = line.to or tablet_recipient
      via  = line.via
  - ba-zi / zi-ga markers flag disbursement (outflow) lines

Output per clause: {commodity, qty, from, to, via, markers, line_no, conf}
"""
import re
import sys
sys.path.insert(0, 'scripts')
from line_extract import extract_tablet, RECV_MARKERS

DATE_WORDS = {'iti', 'mu', 'ba-hun', 'ba-du3', 'mu-ne-di', 'ba-dim2',
              'ezem-mah', 'ezem-an-na', 'ezem-szu-numun', 'u5-bi2-gu7',
              'a2-ki-ti'}


def is_date_line(text):
    t = text.strip()
    if re.match(r'mu\s', t) or t.startswith('iti '):
        return True
    if any(w in t for w in ('ba-hun', 'ba-du3', 'mu-ne-di', 'ba-dim2')):
        return True
    return False


def assemble(text):
    lines = extract_tablet(text)
    clauses = []
    current_from = set()
    tablet_recipient = set()
    # tablet-level single-party fallback
    all_from = set()
    all_to = set()
    for _, _, e in lines:
        all_from |= e['from']
        all_to |= e['to']
    single_from = all_from if len(all_from) == 1 else set()
    # first pass: find the recipient pattern (mu-ku / i3-dab5 / szu ba-ti + name)
    for i, (no, t, e) in enumerate(lines):
        if any(mk in e['markers'] for mk in ('mu-ku', 'i3-dab5', 'szu ba-ti')):
            # recipient = bare names on this line and adjacent lines
            for j in (i - 1, i, i + 1):
                if 0 <= j < len(lines):
                    _, _, ej = lines[j]
                    for n in ej['names']:
                        if n not in DATE_WORDS and not any(
                                mk in n for mk in ('mu-ku', 'i3-dab', 'ba-ti')):
                            tablet_recipient.add(n)
            # a from-party is not the recipient
            tablet_recipient -= e['from']
    tablet_recipient -= all_from
    # second pass: emit clauses
    for no, t, e in lines:
        if is_date_line(t):
            continue
        if e['from']:
            current_from = set(e['from'])
        if not e['qty']:
            continue
        frm = (set(e['from']) or set(e['names']) or set(current_from)
               or set(single_from))
        # bare names on qty lines are sources; drop date words
        frm = {x for x in frm if x not in DATE_WORDS}
        to = set(e['to']) or set(tablet_recipient)
        for comm, qty in e['qty']:
            clauses.append({
                'commodity': comm, 'qty': qty,
                'from': sorted(frm), 'to': sorted(to),
                'via': sorted(e['via']),
                'markers': sorted(e['markers']),
                'line': no,
                'conf': 'high' if (e['from'] or e['to']) else 'medium',
            })
    return clauses


if __name__ == '__main__':
    buf = []
    with open('sources/drehem.atf', encoding='utf-8') as f:
        for line in f:
            if line.startswith('&P100232 '):
                buf = [line]
            elif buf and line.startswith('&P'):
                break
            elif buf:
                buf.append(line)
    for c in assemble(''.join(buf)):
        print(f"{c['commodity']:6s} {c['qty']:3d} | from={c['from']} -> to={c['to']} "
              f"| line {c['line']} [{c['conf']}]")
