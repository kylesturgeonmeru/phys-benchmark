import sys,re,glob,json
sys.path.insert(0,'.')
import pandas as pd
from tbl import *
from parse_abbvie import num
F=json.load(open('filings.json'))
URL={rd:f"https://www.sec.gov/Archives/edgar/data/1570562/{acc.replace('-','')}/{doc}" for form,acc,rd,fd,doc in F['evolus']}
def ql(y,m): return f"{y}Q{(int(m)-1)//3+1}"
def inc_tbl(p):
    d=load(p)
    for t in d.iter('table'):
        rs=rows_of(t)
        labs=[r[0] for r in rs]
        if not any(re.match(r'(Total net revenues?|Net revenues?|Product revenue, net)$',l) for l in labs): continue
        if not any(l.startswith(('Cost of','Product cost','Research','Selling')) for l in labs): continue
        out={}
        for r in rs:
            l=r[0]
            key=None
            if l.startswith('Jeuveau'): key='Jeuveau'
            elif l.startswith('Evolysse'): key='Evolysse'
            elif l.startswith('Product revenue') or l.startswith('Total product revenue'): key='Product'
            elif l.startswith('Service revenue'): key='Service'
            elif re.match(r'(Total net revenues?|Net revenues?)$',l): key='Total'
            if key and key not in out and len(r)>1:
                v=[num(x) for x in r[1:]]
                out[key]=v
        if 'Total' not in out and 'Product' in out: out['Total']=out['Product']
        tot=out.get('Total',[0])[0]
        if tot is not None and tot>=1000 or tot==0: return out   # thousands
    return None

def split_tbl(p):
    d=load(p)
    for t in d.iter('table'):
        rs=rows_of(t)
        if any(r[0].startswith('Evolysse') and len(r)>1 and re.search(r'\d',r[1]) for r in rs) and any(r[0].startswith('Jeuveau') and len(r)>1 and re.search(r'\d',r[1]) for r in rs) and any(r[0].startswith('Total net revenue') for r in rs):
            out={}
            for r in rs:
                if r[0].startswith('Jeuveau') and 'J' not in out: out['J']=[num(x) for x in r[1:]]
                if r[0].startswith('Evolysse') and 'E' not in out: out['E']=[num(x) for x in r[1:]]
            return out
T={};S={}
for p in sorted(glob.glob('cache/evolus_20*')):
    m=re.search(r'evolus_(\d{4})-(\d\d)-(\d\d)_(10-[QK])',p); y,mo,dd,form=m.groups()
    T[(y,mo)]=inc_tbl(p); S[(y,mo)]=split_tbl(p)
rows=[]
def g(d,k,i): 
    v=(d or {}).get(k); return None if v is None or len(v)<=i else v[i]
for (y,mo),t in sorted(T.items()):
    if t is None: continue
    q=ql(y,mo); url=URL[f"{y}-{mo}-{'31' if mo in ('03','12') else '30'}"]
    s=S[(y,mo)]
    if mo=='12':
        t9=T[(y,'09')]; s9=S[(y,'09')]
        tot=t['Total'][0]-t9['Total'][2]
        prod=t['Product'][0]-t9['Product'][2] if 'Product' in t and 'Product' in t9 else tot
        svc=(t.get('Service',[0])[0]or 0)-(t9.get('Service',[0,0,0])[2] if 'Service' in t9 else 0)
        if s and s.get('J'):
            j=s['J'][0]-(s9['J'][2] if s9 else 0) if s9 else None
            e=s['E'][0]-(s9['E'][2] if s9 else 0) if s9 else None
            if j is None:  # Q3 10-Q had no split table
                j=None
        basis='derived: FY less 9M'
    else:
        tot=t['Total'][0]; prod=t['Product'][0] if 'Product' in t else tot
        svc=t['Service'][0] if 'Service' in t else 0
        basis='reported'
    # split
    if s and mo!='12': j,e=s['J'][0],s['E'][0]
    elif s and mo=='12': pass
    else: j,e=prod,0.0
    if mo=='12' and not s: j,e=prod,0.0
    rows.append(dict(company='Evolus',quarter=q,total_net_revenue=tot/1000,product_revenue=prod/1000,toxin_jeuveau=(j or 0)/1000,filler_evolysse=(e or 0)/1000,service_revenue=svc/1000,basis=basis,source_url=url))
# Q1 2019 not in tables (pre-launch): zero revenue
rows.insert(0,dict(company='Evolus',quarter='2019Q1',total_net_revenue=0.0,product_revenue=0.0,toxin_jeuveau=0.0,filler_evolysse=0.0,service_revenue=0.0,basis='reported (pre-launch, Jeuveau launched May 2019)',source_url=URL['2019-03-31']))
df=pd.DataFrame(rows).sort_values('quarter').reset_index(drop=True)
df['toxin_jeuveau']=df['toxin_jeuveau'].round(3)
df.to_pickle('evolus_q.pkl')
pd.set_option('display.width',250)
print(df.drop(columns='source_url').to_string())
