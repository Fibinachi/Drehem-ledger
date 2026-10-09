#!/usr/bin/env python3
"""Build the Drehem ledger SQLite database — the end artifact.

Schema (PLAN.md v0.1):
  tablets: P-number, dates, raw ATF pointer, parse status
  entities: resolved persons/institutions with types + Hilgert validation
  transactions: the ledger proper (from clause assembler)
  balances: entity x commodity x year -> in/out/net
"""
import re, csv, json, sqlite3
from collections import defaultdict, Counter
import sys
sys.path.insert(0, 'scripts')
from clause_assemble import assemble
from clause_balance import tablet_markers, clause_direction, load_officials
from temple_accounts import DIVINE_CORE, INSTIT, FESTIVAL, desub

DB = 'ledger/drehem-ledger.db'

# Sumerian words that are not personal names (verbs, 'total', 'dead', festivals)
NONAME = {'szunigin', 'nigin-ba', 'nigin', 'ba-usz', 'ba-usz2', 'ba-zal',
          'ba-hul', 'ba-du', 'ba-du3', 'szu-gid', 'szu-gid2', 'a-sza',
          'ezem-szul-gi', 'ezem-nin-a-zu', 'ezem-mah', 'ezem-an-na',
          'u4', 'disz', 'kam', 'la2', 'gaba-ri', 'kiszib', 'kiszib3'}


def build_schema(cx):
    cx.executescript('''
    DROP TABLE IF EXISTS tablets;
    DROP TABLE IF EXISTS entities;
    DROP TABLE IF EXISTS transactions;
    DROP TABLE IF EXISTS balances;
    CREATE TABLE tablets (
        pn TEXT PRIMARY KEY,
        king TEXT, year INT, month INT, day INT,
        date_src TEXT,           -- 'catalog' | 'formula' | 'prosopographic' | NULL
        date_conf REAL,
        n_clauses INT DEFAULT 0,
        parse_status TEXT
    );
    CREATE TABLE entities (
        eid INTEGER PRIMARY KEY,
        canon TEXT UNIQUE,       -- desubscripted canonical name
        atf_form TEXT,           -- most common ATF spelling
        etype TEXT,              -- official|divine|institution|person
        hilgert INT DEFAULT 0,   -- 1 if in Hilgert roster
        n_attest INT DEFAULT 0,
        first_year TEXT, last_year TEXT
    );
    CREATE TABLE transactions (
        txn_id INTEGER PRIMARY KEY,
        pn TEXT REFERENCES tablets(pn),
        clause_idx INT, line_no INT,
        king TEXT, year INT,
        from_eid INT REFERENCES entities(eid),
        to_eid INT REFERENCES entities(eid),
        via_eid INT REFERENCES entities(eid),
        commodity TEXT, qty INT,
        txn_type TEXT,           -- receipt|disbursement|transfer
        conf TEXT,
        raw_from TEXT, raw_to TEXT
    );
    CREATE TABLE balances (
        eid INT, commodity TEXT, king TEXT, year INT,
        inflow INT DEFAULT 0, outflow INT DEFAULT 0,
        PRIMARY KEY (eid, commodity, king, year)
    );
    CREATE INDEX idx_txn_pn ON transactions(pn);
    CREATE INDEX idx_txn_from ON transactions(from_eid);
    CREATE INDEX idx_txn_to ON transactions(to_eid);
    CREATE INDEX idx_txn_date ON transactions(king, year);
    ''')
    cx.commit()


def main():
    import os
    os.makedirs('ledger', exist_ok=True)
    cx = sqlite3.connect(DB)
    build_schema(cx)

    # dates
    dates, dsrc, dconf = {}, {}, {}
    with open('sources/drehem_dates.csv') as f:
        for row in csv.DictReader(f):
            m = re.match(r'([^.]+)\.(\d+)\.(\d+)\.(\d+)', row['dates_referenced'] or '')
            if m:
                dates[row['P']] = (m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)))
                dsrc[row['P']] = 'catalog'; dconf[row['P']] = 1.0
    for pn, r in json.load(open('sources/redated.json')).items():
        k, y = r['date'].split('.')
        dates[pn] = (k, int(y), None, None)
        dsrc[pn] = 'formula'; dconf[pn] = r['conf']

    officials = load_officials()
    roster = set()
    try:
        roster = {desub(x) for x in json.load(open('sources/hilgert_roster_all.json'))}
    except FileNotFoundError:
        pass

    # entity registry
    ents = {}  # canon -> dict
    def eid_for(name):
        c = desub(name)
        if c in NONAME:
            return None
        if c not in ents:
            d = c
            if d in DIVINE_CORE:
                et = 'divine'
            elif name in INSTIT or name in FESTIVAL or d in INSTIT:
                et = 'institution'
            elif c in officials or 'ab-ba-sa-ga' in c:
                et = 'official'
            else:
                et = 'person'
            ents[c] = {'canon': c, 'atf': name, 'etype': et,
                       'hilgert': 1 if c in roster else 0,
                       'n': 0, 'years': set()}
        return c

    # pass 1: collect entities + tablet rows
    tablets = {}
    txns = []
    buf, cur = [], None
    with open('sources/drehem.atf', encoding='utf-8') as f:
        for line in f:
            if line.startswith('&P') and buf:
                t = ''.join(buf)
                clauses = assemble(t)
                recv, outm = tablet_markers(t)
                king, year, month, day = dates.get(cur, (None, None, None, None))
                tablets[cur] = (king, year, month, day, dsrc.get(cur),
                                dconf.get(cur), len(clauses))
                for ci, c in enumerate(clauses):
                    for n in c['from'] + c['to'] + c['via']:
                        cc = eid_for(n)
                        if cc is None:
                            continue
                        ents[cc]['n'] += 1
                        if year:
                            ents[cc]['years'].add((king, year))
                    d = clause_direction(c, recv, outm, officials)
                    txns.append((cur, ci, c['line'], king, year,
                                 c['from'], c['to'], c['via'],
                                 c['commodity'], c['qty'], d, c['conf']))
                buf, cur = [line], line[1:].split()[0]
            else:
                buf.append(line)

    # write tablets
    cx.executemany(
        'INSERT INTO tablets VALUES (?,?,?,?,?,?,?,?,?)',
        [(pn, k, y, mo, da, ds, dc, nc, 'parsed' if nc else 'no_clauses')
         for pn, (k, y, mo, da, ds, dc, nc) in tablets.items()])
    # write entities
    for c, e in ents.items():
        ys = sorted(e['years'])
        cx.execute(
            'INSERT INTO entities (canon, atf_form, etype, hilgert, n_attest, first_year, last_year)'
            ' VALUES (?,?,?,?,?,?,?)',
            (c, e['atf'], e['etype'], e['hilgert'], e['n'],
             f"{ys[0][0]}.{ys[0][1]}" if ys else None,
             f"{ys[-1][0]}.{ys[-1][1]}" if ys else None))
    cx.commit()
    print(f"tablets: {len(tablets)}, entities: {len(ents)}, "
          f"raw transactions: {len(txns)}")

    # map names to eids
    emap = {r[0]: r[1] for r in cx.execute('SELECT canon, eid FROM entities')}
    def to_eid(names):
        return emap.get(desub(names[0])) if names else None

    # write transactions (only directed ones)
    tmap = {'in': 'receipt', 'out': 'disbursement', 'transfer': 'transfer'}
    rows = []
    for (pn, ci, ln, k, y, fr, to, via, comm, qty, d, conf) in txns:
        if d not in tmap:
            continue
        rows.append((pn, ci, ln, k, y, to_eid(fr), to_eid(to), to_eid(via),
                     comm, qty, tmap[d], conf,
                     ','.join(fr[:3]), ','.join(to[:3])))
    cx.executemany(
        'INSERT INTO transactions (pn, clause_idx, line_no, king, year, from_eid, to_eid,'
        ' via_eid, commodity, qty, txn_type, conf, raw_from, raw_to)'
        ' VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', rows)
    cx.commit()
    print(f"directed transactions written: {len(rows)}")

    # balances
    cx.executescript('''
    INSERT INTO balances (eid, commodity, king, year, inflow, outflow)
    SELECT to_eid, commodity, king, year, SUM(qty), 0
    FROM transactions WHERE txn_type IN ('receipt','transfer') AND to_eid IS NOT NULL
      AND king IS NOT NULL
    GROUP BY to_eid, commodity, king, year;
    INSERT INTO balances (eid, commodity, king, year, inflow, outflow)
    SELECT from_eid, commodity, king, year, 0, SUM(qty)
    FROM transactions WHERE txn_type IN ('disbursement','transfer') AND from_eid IS NOT NULL
      AND king IS NOT NULL
    GROUP BY from_eid, commodity, king, year
    ON CONFLICT(eid, commodity, king, year)
    DO UPDATE SET outflow = outflow + excluded.outflow;
    ''')
    cx.commit()
    n_bal = cx.execute('SELECT COUNT(*) FROM balances').fetchone()[0]
    print(f"balance rows: {n_bal}")
    print(f"database: {DB}")
    cx.close()


if __name__ == '__main__':
    main()
