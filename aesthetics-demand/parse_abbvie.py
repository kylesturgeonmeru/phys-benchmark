import sys,re,json,glob,os
sys.path.insert(0,'.')
from tbl import *
def num(s):
    s=s.replace(',','').replace('$','').strip()
    if s in('—','-','–'): return 0.0
    neg=s.startswith('(')
    s=s.strip('()')
    try: v=float(s)
    except: return None
    return -v if neg else v
# ---------- AbbVie
def abbvie_tbl(p):
    d=load(p)
    for t in find_tables(d,r'Botox Cosmetic'):
        s=str(t)
        if 'Percent change' in s or 'Percent' in s[:400]: continue
        if any(r and r[0].startswith('Botox Cosmetic') for r in t):
            # parse
            out={};prod=None
            for r in t:
                lab=r[0]
                if lab.startswith(('Botox Cosmetic','Juvederm','Other Aesthetics')):
                    prod=re.sub(r'\s*\(a\)','',lab).strip(); lab=r[1]; vals=r[2:]
                elif prod and lab in('International',):
                    vals=r[1:]
                else: continue
                geo='US' if lab=='United States' else 'Intl'
                out[(prod,geo)]=[num(v) for v in vals]
            if out: return out
    return None
def allergan_tables(p):
    """returns {('US'|'Intl', period_kind): {product:[cur,prior]}}"""
    d=load(p); out={}
    for t in find_tables(d,r'Botox.{0,3} Cosmetics'):
        if not any(r[0].startswith('Total Medical Aesthetics') for r in t): continue
        hdr=t[0][0]
        kind='3M' if 'Three' in hdr else ('6M' if 'Six' in hdr else ('9M' if 'Nine' in hdr else 'FY'))
        geo='Intl' if any('Currency' in c for c in t[1]) else 'US'
        # FY table 1 is a 3-year US table with '$ Change'
        d_={}
        for r in t:
            lab=r[0]
            for key,nm in (('Total Medical Aesthetics','TMA'),('Botox','BC'),('Juvederm','JV')):
                if lab.startswith(key) and (nm!='BC' or 'Cosmetics' in lab) and nm not in d_:
                    d_[nm]=num(r[1])
        out.setdefault((geo,kind),d_)
    return out
