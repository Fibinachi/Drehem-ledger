#!/usr/bin/env python3
"""Nanna temple account: reconstruct temple inflows from Drehem's outflow records.

Temples don't keep books in this archive — but Drehem records every animal
sent TO them. Recipients: divine names ({d}X-še3), temples (e2 {d}X),
festivals (a2-ki-ti), and cultic purposes (siskur2 offerings).

Output: per-year, per-commodity inflows to each divine/institutional account,
plus which officials disbursed them.
"""
import re, csv, json
from collections import defaultdict, Counter
import sys
sys.path.insert(0, 'scripts')
from mass_balance_pilot import VAL, COMMOD, NAME_PAT, clean, is_name, base_comm
from inflow_pilot import tablet_lines

DIVINE_CORE = {'nanna','en-lil2','da-gan','iszkur','szara2','mes-lam','inanna',
               'nin-urta','nin-gal','en-ki','utu','nisaba','nin-hur-sag-ga',
               'dumu-zi','gesztin-an-na','nin-a-zu','nin-sun2','lugal-banda'}
INSTIT = {'e2-gal','na-gab2-tum','e2-muhaldim','e2-kikken2','e2-uz-ga'}
FESTIVAL = {'a2-ki-ti','ezem-mah','ezem-szu-numun','ezem-an-na'}
CULTIC = {'siskur2','sa2-du11'}

def desub(s): return re.sub(r'[0-9]','',s)

def get_recipients(text):
    """Names in -še3 slots + bare divine/institutional names."""
    out = set()
    for raw in text.split('\n'):
        l = raw.strip()
        if not l or l[0] in '>@#&$': continue
        l = re.sub(r'^\d+\.\s*','',l)
        if not l or l.startswith(('@','&','$','>>','#')): continue
        # strip determinatives for matching but keep them out of names
        l2 = re.sub(r'\{d\}','',l).replace('{ki}','')
        for m in re.finditer(r'\b(%s)-še3\b' % NAME_PAT, l2):
            c = clean(m.group(1))
            if is_name(c): out.add(c)
        # bare divine/institutional tokens anywhere
        for tok in re.findall(r'[a-z][a-z0-9\-\.šĝḫŋřž]+', l2):
            c = clean(tok)
            d = desub(c)
            if d in DIVINE_CORE or c in INSTIT or c in FESTIVAL:
                out.add(c)
    return out

def get_froms(text):
    out=set()
    for raw in text.split('\n'):
        l=raw.strip()
        if not l or l[0] in '>@#&$': continue
        l=re.sub(r'^\d+\.\s*','',l)
        if not l or l.startswith(('@','&','$','>>','#')): continue
        l2=re.sub(r'\{(d|ki)\}','',l)
        for pat in (r'\bki (%s)(?:-ta)?(?:\s|$)'%NAME_PAT, r'\b(%s)-ta\b'%NAME_PAT):
            for m in re.finditer(pat,l2):
                c=re.sub(r'-ta$','',clean(m.group(1)))
                if is_name(c) and len(c)>=4: out.add(c)
    return out

def get_qtys(text):
    qtys=defaultdict(int)
    for l in tablet_lines(text):
        for m in re.finditer(r'((?:\d+\([a-z0-9]+\)\s*)+)\s*([a-z][a-z0-9\-\.šĝḫŋřž]*)', l):
            comm=base_comm(m.group(2))
            if comm not in COMMOD: continue
            qty=sum(int(q.group(1))*VAL.get(q.group(2),0) for q in re.finditer(r'(\d+)\(([a-z0-9]+)\)',m.group(1)))
            if qty: qtys[comm]+=qty
    return qtys

def acct(n):
    d=desub(n)
    if d in DIVINE_CORE: return 'DIVINE:'+d
    if n in INSTIT: return 'INSTIT:'+n
    if n in FESTIVAL: return 'FEST:'+n
    return None

def main():
    dates={}
    with open('sources/drehem_dates.csv') as f:
        for row in csv.DictReader(f):
            m=re.match(r'([^.]+)\.(\d+)\.',row['dates_referenced'] or '')
            dates[row['P']]=(m.group(1),int(m.group(2))) if m else (None,None)

    flows=defaultdict(int)   # (acct, comm, king, year) -> qty
    disb=Counter()            # (from, acct) pairs
    n_tablets=0
    buf,cur=[],None
    with open('sources/drehem.atf',encoding='utf-8') as f:
        for line in f:
            if line.startswith('&P') and buf:
                t=''.join(buf)
                recips={r for r in get_recipients(t) if acct(r)}
                if recips:
                    qtys=get_qtys(t); froms=get_froms(t)
                    king,year=dates.get(cur,(None,None))
                    n_tablets+=1
                    for r in recips:
                        a=acct(r)
                        for comm,qty in qtys.items():
                            flows[(a,comm,king,year)]+=qty
                        for s in froms:
                            if 'ab-ba-sa6-ga' in s or True:
                                disb[(s,a)]+=1
                buf,cur=[line],line[1:].split()[0]
            else: buf.append(line)

    print(f"tablets with divine/institutional recipients: {n_tablets}")
    # Nanna account, all years
    nanna_years=defaultdict(lambda: defaultdict(int))
    for (a,comm,king,year),q in flows.items():
        if a=='DIVINE:nanna' and king=='Amar-Suen' and year:
            nanna_years[year][comm]+=q
    print("\nNanna temple inflows (Amar-Suen, by commodity):")
    print(f"{'yr':>3} {'udu':>8} {'gu4':>7} {'masz2':>7} {'sila4':>7} {'u8':>7}")
    for y in range(1,10):
        v=nanna_years[y]
        print(f"{y:>3} {v['udu']:>8,} {v['gu4']:>7,} {v['masz2']:>7,} {v['sila4']:>7,} {v['u8']:>7,}")
    # top divine accounts overall
    tot=Counter()
    for (a,comm,king,year),q in flows.items(): tot[a]+=q
    print("\ntop divine/institutional accounts (all commodities, all years):")
    for a,q in tot.most_common(12): print(f"  {q:>10,}  {a}")
    # who disburses to Nanna?
    print("\ntop disbursers to DIVINE:nanna:")
    dn=Counter({s:c for (s,a),c in disb.items() if a=='DIVINE:nanna'})
    for s,c in dn.most_common(10): print(f"  {c:5d}  {s}")
    json.dump([{'acct':a,'comm':c,'king':k,'year':y,'qty':q}
               for (a,c,k,y),q in flows.items() if q],
              open('sources/temple_accounts.json','w'), indent=1)

if __name__=='__main__': main()
