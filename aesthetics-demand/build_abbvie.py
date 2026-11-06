import sys,re,json,glob,pickle
sys.path.insert(0,'.')
import pandas as pd
from tbl import *
from parse_abbvie import num   # re-runs parse (cheap enough)
from parse_abbvie import abbvie_tbl, allergan_tables
F=json.load(open('filings.json'))
CIK={"abbvie":"1551152","allergan":"1578845"}
URL={}
for co in('abbvie','allergan'):
    for form,acc,rd,fd,doc in F[co]:
        URL[(co,rd)]=f"https://www.sec.gov/Archives/edgar/data/{CIK[co]}/{acc.replace('-','')}/{doc}"
rows=[]
def add(co,q,prod,geo,val,basis,url,note=''):
    rows.append(dict(company=co,quarter=q,product=prod,region=geo,revenue_usd_m=val,basis=basis,source_url=url,note=note))
def ql(y,m): return f"{y}Q{(int(m)-1)//3+1}"
# ---- Allergan plc (2019Q1..2020Q1)
AG={}
for p in sorted(glob.glob('cache/allergan_201[9]*')+glob.glob('cache/allergan_2020*')):
    m=re.search(r'allergan_(\d{4})-(\d\d)-(\d\d)_',p); y,mo,dd=m.groups()
    AG[(y,mo)]=allergan_tables(p)
nm={'BC':'Botox Cosmetic','JV':'Juvederm Collection'}
for (y,mo),T in AG.items():
    if (y,mo)==('2018','12'): continue
    url=URL[('allergan',f'{y}-{mo}-{"31" if mo in("03","12") else "30"}')]
    for geo in('US','Intl'):
        for k,pn in (('BC','Botox Cosmetic'),('JV','Juvederm Collection'),('OT','Other Aesthetics')):
            if mo=='12':
                fy=T[(geo,'FY')]; ytd=AG[(y,'09')][(geo,'9M')]
                get=lambda d:(d['TMA']-d['BC']-d['JV']) if k=='OT' else d[k]
                add('Allergan plc',ql(y,mo),pn,geo,round(get(fy)-get(ytd),1),'derived: FY less 9M',url,'Q4 = 10-K full year minus 9M YTD from Q3 10-Q'+('; Other = Total Medical Aesthetics less Botox Cosmetics less Juvederm (includes breast implants, Alloderm, CoolSculpting, skin care, Kybella)' if k=='OT' else ''))
            else:
                d=T[(geo,'3M')]
                v=(d['TMA']-d['BC']-d['JV']) if k=='OT' else d[k]
                add('Allergan plc',ql(y,mo),pn,geo,round(v,1),'reported' if k!='OT' else 'derived: segment table',url,'' if k!='OT' else 'Other = Total Medical Aesthetics less Botox Cosmetics less Juvederm (includes breast implants, Alloderm, CoolSculpting, skin care, Kybella)')
# ---- AbbVie 2020Q2..
AV={}
for p in sorted(glob.glob('cache/abbvie_20[2]*')):
    m=re.search(r'abbvie_(\d{4})-(\d\d)-(\d\d)_(10-[QK])',p); y,mo,dd,form=m.groups()
    AV[(y,mo)]=abbvie_tbl(p)
for (y,mo),T in sorted(AV.items()):
    if T is None: continue
    url=URL[('abbvie',f'{y}-{mo}-{"31" if mo in("03","12") else "30"}')]
    for (pn,geo),vals in T.items():
        if mo=='12':
            q3=AV[(y,'09')][(pn,geo)]
            fy=vals[0]; ytd9=q3[2] if len(q3)>=4 else None
            add('AbbVie',ql(y,mo),pn,geo,fy-ytd9,'derived: FY less 9M',url,'Q4 = 10-K full year minus 9M YTD from Q3 10-Q')
        else:
            note='Stub: Allergan included from 8 May 2020 only' if (y,mo)==('2020','06') else ''
            add('AbbVie',ql(y,mo),pn,geo,vals[0],'reported' if note=='' else 'reported (partial quarter)',url,note)
df=pd.DataFrame(rows)
df.to_pickle('abbvie_long.pkl')
pd.set_option('display.width',250)
pv=df.pivot_table(index='quarter',columns=['product','region'],values='revenue_usd_m',aggfunc='first')
print(pv.to_string())
