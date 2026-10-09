#!/usr/bin/env python3
"""Date the undated: learn year formulae from dated tablets, apply to the rest.
Truly dateless tablets fall back to official active-year ranges."""
import re, csv, json
from collections import defaultdict, Counter
from difflib import SequenceMatcher

dates = {}
with open('sources/drehem_dates.csv') as f:
    for row in csv.DictReader(f):
        m = re.match(r'([^.]+)\.(\d+)\.', row['dates_referenced'] or '')
        if m:
            dates[row['P']] = (m.group(1), int(m.group(2)))

formulae = defaultdict(Counter)
mu_of = {}
buf, cur = [], None
with open('sources/drehem.atf', encoding='utf-8') as f:
    for line in f:
        if line.startswith('&P') and buf:
            t = ''.join(buf)
            mus = []
            for raw in t.split('\n'):
                l = raw.strip()
                m = re.match(r'\d+\.\s*(mu\s.+)$', l)
                if m:
                    mu_n = re.sub(r'[\[\]]', '', m.group(1)).strip()
                    mus.append(mu_n)
                    if cur in dates:
                        formulae[dates[cur]][mu_n] += 1
            mu_of[cur] = mus
            buf, cur = [line], line[1:].split()[0]
        else:
            buf.append(line)

ref = {}
for ky, c in formulae.items():
    ref[f"{ky[0]}.{ky[1]}"] = [mu for mu, n in c.most_common() if n >= 2]
print(f"year formulae learned for {len(ref)} king-years")
json.dump(ref, open('sources/year_formulae.json', 'w'), indent=1, ensure_ascii=False)

# match undated mu-lines against reference (fuzzy, damage-tolerant)
flat = [(ky, v) for ky, vs in ref.items() for v in vs]
results = {}
for pn, mus in mu_of.items():
    if pn in dates or not mus:
        continue
    best = (0, None)
    for mu in mus:
        for ky, v in flat:
            r = SequenceMatcher(None, mu, v).ratio()
            if r > best[0]:
                best = (r, ky)
    if best[0] >= 0.75:
        results[pn] = {'date': best[1], 'conf': round(best[0], 3), 'via': 'formula'}
print(f"dated via formula matching: {len(results)}")

json.dump(results, open('sources/redated.json', 'w'), indent=1)
still = [pn for pn in mu_of if pn not in dates and pn not in results]
print(f"still undated: {len(still)}")
json.dump(still, open('sources/still_undated.json', 'w'))
